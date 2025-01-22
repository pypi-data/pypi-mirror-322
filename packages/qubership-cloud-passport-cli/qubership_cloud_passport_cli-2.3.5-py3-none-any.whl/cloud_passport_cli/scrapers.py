from __future__ import annotations
import logging
import base64
from cryptography.fernet import Fernet
from json import loads
from yaml import safe_load

from urllib.parse import urlsplit
from kubernetes import dynamic
from collector import CollectorInfo
from connect import Connect
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)

class ScrapeInfo():
    isinstance = None

    def __new__(cls, connect:Connect, key:Fernet) -> ScrapeInfo:
        if ScrapeInfo.isinstance is None:
            ScrapeInfo.isinstance = super().__new__(cls)
            ScrapeInfo.connect = connect
            ScrapeInfo.key = key
            ScrapeInfo.scrapers = {cls.__name__.split("Scrape")[1].lower():cls.get_info for cls in ScrapeInfo.__subclasses__()}
            return ScrapeInfo.isinstance

    def get_scrape(self, type:str, namespace:str) -> ScrapeInfo:
        return self.scrapers[type](self, namespace)
    
    def get_info(namespase:str) -> None:
        NotImplemented

class ScrapeKafka(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        scrape_versions = {True: ScrapeKafka.get_info_v1, False: ScrapeKafka.get_info_v2}

        custom_kafka = self.connect.resources.search(kind='KafkaService')[0].get(namespace=namespace, name='kafka')
        version = 'kafka' in dir(custom_kafka.spec)
        return scrape_versions[version](self, namespace)

    def common_get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="kafka")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "kafka-client":
               data['port'] = port.port
        data['internal'] = f"{services.metadata.name}.{namespace}:{port.port}"
        
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='kafka-secret')
        data_sensitive['admin'] = {'type':'usernamePassword'}
        data_sensitive['client'] = {'type':'usernamePassword'}
        data_sensitive['url'] = {'type':'secret'}
        data_sensitive['client']['username'] = base64.b64decode(secrets.data['client-username'].encode('utf-8')).decode('utf-8')
        data_sensitive['client']['password'] = base64.b64decode(secrets.data['client-password'].encode('utf-8')).decode('utf-8')
        data_sensitive['admin']['username'] = base64.b64decode(secrets.data['admin-username'].encode('utf-8')).decode('utf-8')
        data_sensitive['admin']['password'] = base64.b64decode(secrets.data['admin-password'].encode('utf-8')).decode('utf-8')
        data_sensitive['url']['url'] = f"kafka://{ data_sensitive['client']['username']}:{data_sensitive['client']['password']}@{data['service_name']}.{data['namespace']}:{data['port']}"

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

    def get_info_v1(self, namespace:str) -> CollectorInfo:
        collector = ScrapeKafka.common_get_info(self, namespace)
        custom_kafka = self.connect.resources.search(kind='KafkaService')[0].get(namespace=namespace, name='kafka')
        collector.data['enable_ssl'] = custom_kafka.spec.kafka.disableSecurity
        return collector

    def get_info_v2(self, namespace:str) -> CollectorInfo:
        collector = ScrapeKafka.common_get_info(self, namespace)
        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="kafka")
        collector.data['enable_ssl'] = services.spec.disableSecurity if services.spec.disableSecurity else False
        return collector

class ScrapeZookeeper(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="zookeeper")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "zookeeper-client":
               data['port'] = port.port
        data['internal'] = f"{services.metadata.name}.{namespace}:{data['port']}"

        collector.data = data
        return collector

class ScrapeRabbitmq(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="rabbitmq")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "5672-tcp":
               data['port'] = port.port
            elif port.name == "15672-tcp":
               data['port_statistics'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"
        
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='rabbitmq-default-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['user'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapePostgres(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="pg-patroni")
        services_ro = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="pg-patroni-ro")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "pg-patroni":
               data['port'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"
        data['internal'] = f"{services.metadata.name}.{namespace}:{data['port']}"
        
        data['service_name_ro'] = services_ro.metadata.name
        for port in services_ro.spec.ports:
            if port.name == "pg-patroni":
               data['port_ro'] = port.port
        data['host_name_ro'] = f"{services_ro.metadata.name}.{namespace}"
        data['internal_ro'] = f"{services_ro.metadata.name}.{namespace}:{data['port_ro']}"

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='postgres-credentials')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['url'] = {'type':'secret'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        data_sensitive['url']['url'] = f"postgresql://{data_sensitive['creds']['username']}:{data_sensitive['creds']['password'] }@{data['service_name']}.{data['namespace']}:{data['port']}"

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeMongodb(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="mongos")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "mongo":
               data['port'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"

        try:
            secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='mongodb-root-credentials')
        except dynamic.exceptions.NotFoundError:
            secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='mongodb-root-credentials.v1')

        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password'] = base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeOpensearch(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="opensearch")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "http":
               data['port'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='opensearch-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeClickhouse(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}
        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="clickhouse-cluster")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "tcp":
               data['port'] = port.port
            elif port.name == "http":
               data['port_jdbc'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='clickhouse-operator-credentials')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeArangodb(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="arangodb")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "arangodb":
               data['port'] = port.port
        data['host_name'] = f"{services.metadata.name}.{namespace}"

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='arangodb-root-password')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['password'] = base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['username'] = 'root'

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeNifi(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data['namespace'] = namespace
        collector.data = data
        return collector
    
class ScrapeMaas(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="maas-service")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "web":
               data['port'] = port.port
        data['internal'] = f"http://{services.metadata.name}.{namespace}:{data['port']}"
        try:
            ingress = self.connect.resources.get(api_version='networking.k8s.io/v1', kind='Ingress').get(namespace=namespace, name='maas-service')
            for rule in  ingress.spec.rules:
                data['service'] = f'https://{rule.host}'
        except dynamic.exceptions.NotFoundError:
            data['service'] = 'Undefined'
            #logging.info("Ingress maas-service not found ")
        collector.data = data
        return collector
    
class ScrapeDbaas(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="dbaas-aggregator")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "web":
               data['port'] = port.port
        data['internal'] = f"http://{services.metadata.name}.{namespace}:{data['port']}"
        try:
            ingress = self.connect.resources.get(api_version='networking.k8s.io/v1', kind='Ingress').get(namespace=namespace, name='aggregator')
            for rule in  ingress.spec.rules:
                data['service'] = f'https://{rule.host}'
        except dynamic.exceptions.NotFoundError:
            data['service'] = 'Undefined'
            #logging.info("Ingress dbaas aggregator not found ")

        deployment = self.connect.resources.get(api_version='v1', kind='Deployment').get(namespace=namespace, name="dbaas-aggregator")
        #for cluster in safe_load(deployment.metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']):
        try:
            applied_configuration = safe_load(deployment.metadata.annotations['kubectl.kubernetes.io/last-applied-configuration'])
        except AttributeError:
            applied_configuration = deployment
        for conf in applied_configuration['spec']['template']['spec']['containers'][0]['env']:
            if conf['name']=='PRODUCTION_MODE':
                data['production_mode'] = conf['value']
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='dbaas-security-configuration-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = 'cluster-dba'
        data_sensitive['creds']['password'] = loads(base64.b64decode(secrets.data['users.json'].encode('utf-8')).decode('utf-8'))[data_sensitive['creds']['username']]['password']

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeDashboard(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        resources = [{'api_version':'networking.k8s.io/v1','kind':'Ingress','name':'kubernetes-dashboard'},{'api_version':'route.openshift.io/v1','kind':'Route','name':'console'}]
        
        data['service'] = 'Undefined'
        for item in resources:
            
            try:
                services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name=item['name'])
                data['namespace'] = namespace
                data['service_name'] = services.metadata.name
                ingress = self.connect.resources.get(api_version=item['api_version'], kind=item['kind']).get(namespace=namespace, name=item['name'])
                if 'rules' in ingress.spec.keys():
                    for rule in  ingress.spec.rules:
                        data['service'] = f'https://{rule.host}'
                else:
                    data['service'] = f'https://{ingress.spec.host}'
            except dynamic.exceptions.NotFoundError:
                continue

        collector.data = data
        return collector
    
class ScrapeStreaming(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="streaming-platform")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "kafka-connect-http":
               data['port'] = port.port
        data['internal'] = f"http://{services.metadata.name}.{namespace}:{data['port']}"

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='streaming-platform-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['streaming-platform-auth-username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['streaming-platform-auth-password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeVault(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
    
        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="vault-service")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        try:
            ingress = self.connect.resources.get(api_version='networking.k8s.io/v1', kind='Ingress').get(namespace=namespace, name='vault-service')
            for rule in  ingress.spec.rules:
                data['service'] = f'https://{rule.host}'
        except dynamic.exceptions.NotFoundError:
            data['service'] = 'Undefined'
            #logging.info("Ingress vault-service not found ")

        collector.data = data
        return collector
    
class ScrapeKeycloak(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
    
        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="infra-keycloak")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "kafka-connect-http":
               data['port'] = port.port
        data['internal'] = f"http://{services.metadata.name}.{namespace}:{data['port']}"

        collector.data = data
        return collector
    
class ScrapeCloud(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        configmap = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name="cluster-info")
        for cluster in safe_load(configmap['data']['kubeconfig'])['clusters']:
            server = cluster['cluster']['server']
        server = urlsplit(server)
        data['api_host'] = server.hostname
        data['api_port'] = server.port
        data['protocol'] =  server.scheme  

        collector.data = data
        return collector

class ScrapeKubeconfig(ScrapeInfo):
    def get_info(self, kubeconfig:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        with open(kubeconfig, mode="r", encoding="utf-8") as schema:
            schema_date = safe_load(schema)

        server = urlsplit(schema_date['clusters'][0]['cluster']['server'])
        data['api_host'] = server.hostname
        data['api_port'] = server.port
        data['protocol'] =  server.scheme  
        data['name'] =  schema_date['clusters'][0]['name']  

        collector.data = data
        return collector

class ScrapeConsul(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="consul-server")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "http":
               data['port'] = port.port
        data['internal'] = f"http://{services.metadata.name}.{namespace}:{data['port']}"
        try:
            ingress = self.connect.resources.get(api_version='networking.k8s.io/v1', kind='Ingress').get(namespace=namespace, name='consul-ingress')
            for rule in  ingress.spec.rules:
                data['service'] = f'https://{rule.host}'
        except dynamic.exceptions.NotFoundError:
            data['service'] = 'Undefined'
            #logging.info("Ingress consul-ingress not found ")
        data['consul_enabled'] = 'true'

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='consul-bootstrap-acl-token')
        data_sensitive['creds'] = {'type':'secret'}
        data_sensitive['creds']['token']= base64.b64decode(secrets.data['token'].encode('utf-8')).decode('utf-8')

        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeMonitoring(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="grafana-service")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        resources = [{'api_version':'networking.k8s.io/v1','kind':'Ingress'},{'api_version':'route.openshift.io/v1','kind':'Route'}]
        data['service'] = 'Undefined'
        for item in resources:
            try:
                ingress = self.connect.resources.get(api_version=item['api_version'], kind=item['kind']).get(namespace=namespace, name='platform-monitoring-grafana')
                if 'rules' in ingress.spec.keys():
                    for rule in  ingress.spec.rules:
                        data['service'] = f'https://{rule.host}'
                else:
                    data['service'] = f'https://{ingress.spec.host}'
            except (dynamic.exceptions.NotFoundError, dynamic.exceptions.ResourceNotFoundError):
                continue
            #logging.info("Ingress om-monitoring-grafana not found ")
            
        if self.connect.resources.get(api_version='v1', kind='Pod').get(namespace=namespace, label_selector="app.kubernetes.io/name in (victoriametrics, vmalert)").items:
            data['type'] = "VictoriaDB"
        elif self.connect.resources.get(api_version='v1', kind='Pod').get(namespace=namespace, label_selector="app.kubernetes.io/name in (prometheus, Prometheus-operator, prometheus-k8s)").items:
            data['type'] = "Prometheus"
        else:
            data['type'] = "Undefined"

        data['monitoring_enabled'] = 'true'
        collector.data = data
        return collector

class ScrapeTracing(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, label_selector="app.kubernetes.io/component=query")
        services = services.items[0]
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        try:
            ingress = self.connect.resources.get(api_version='networking.k8s.io/v1', kind='Ingress').get(namespace=namespace, label_selector="app.kubernetes.io/component=query")
            ingress = ingress.items[0]
            for rule in ingress.spec.rules:
                data['service'] = f'https://{rule.host}'
        except dynamic.exceptions.NotFoundError:
            data['service'] = 'Undefined'
            #logging.info("Ingress vault-service not found ")
        data['tracing_enabled'] = 'true'
        collector.data = data
        return collector

class ScrapeCassandra(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}
        data_sensitive ={}

        services = self.connect.resources.get(api_version='v1', kind='Service').get(namespace=namespace, name="cassandra")
        data['namespace'] = namespace
        data['service_name'] = services.metadata.name
        for port in services.spec.ports:
            if port.name == "cql-port":
               data['port'] = port.port
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace)
        secrets = filter(lambda secret: 'cassandra-secret' in secret.metadata['name'], secrets.items)
        secrets = list(secrets)[0]
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['url'] = {'type':'secret'}
        data_sensitive['creds']['username'] = base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password'] = base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        data_sensitive['url']['url'] = f"cassandra://{data_sensitive['creds']['username']}:{data_sensitive['creds']['password']}@{data['service_name']}.{data['namespace']}:{data['port']}"


        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector


class ScrapeProvider_Connect(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name="discovery-cli-sa-token")
        return base64.b64decode(secrets.data['token'].encode('utf-8')).decode('utf-8')
    

class ScrapeProvider(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        sub_collectors = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, label_selector="discovery.cli.io/type=external")
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, label_selector="discovery.cli.io/type=external")
        sec_sa = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace='default', name='project-sa-token')

        collector.data_sensitive['cloud-deploy-sa-token']= {}
        collector.data_sensitive['cloud-deploy-sa-token']['creds'] = {'type':'secret'}
        collector.data_sensitive['cloud-deploy-sa-token']['creds']['token'] = base64.b64decode(sec_sa.data['token'].encode('utf-8')).decode('utf-8')


        for config in config_map.to_dict()['items'] + secrets.to_dict()['items']:
            sub_collectors[config['metadata']['labels']['discovery.cli.io/subtype']] = self.get_scrape(config['metadata']['labels']['discovery.cli.io/subtype'], namespace)
        
        for sub in sub_collectors:
            collector.data[sub] = sub_collectors[sub].data
            collector.data_sensitive[sub] =  sub_collectors[sub].data_sensitive
        return collector
    
class ScrapeSmtp(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive = {}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='smtp-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='smtp-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeDns(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='dns-configmap')
        data = safe_load(config_map['data']['conf'])
        
        collector.data = data
        return collector

class ScrapeCoreExternal(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='core-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='core-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['tenant_admin_login'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['tenant_admin_password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeGraylog(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='graylog-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='graylog-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeStorage(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='storage-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='storage-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeCmdb(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='cmdb-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='cmdb-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['token'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['user'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeVaultExternal(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}
        
        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='vault-configmap')
        data = safe_load(config_map['data']['conf'])
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector

class ScrapeMaasExternal(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}
        
        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='maas-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
    
class ScrapeMonitoringExternal(ScrapeInfo):
    def get_info(self, namespace:str) -> CollectorInfo:
        collector = CollectorInfo(self.key)
        data_sensitive ={}
        data = {}

        config_map = self.connect.resources.get(api_version='v1', kind='ConfigMap').get(namespace=namespace, name='monitoring-configmap')
        data = safe_load(config_map['data']['conf'])

        secrets = self.connect.resources.get(api_version='v1', kind='Secret').get(namespace=namespace, name='monitoring-secret')
        data_sensitive['creds'] = {'type':'usernamePassword'}
        data_sensitive['creds']['password']= base64.b64decode(secrets.data['password'].encode('utf-8')).decode('utf-8')
        data_sensitive['creds']['username']= base64.b64decode(secrets.data['username'].encode('utf-8')).decode('utf-8')
        
        collector.data = data
        collector.data_sensitive = data_sensitive
        return collector
