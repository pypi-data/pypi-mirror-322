from __future__ import annotations
import logging
from connect import Connect
import sys

logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)

class Discover():  
    def __init__(self, connect:Connect, scrapers:list) -> None:
        self.connect = connect
        self.scrapers = scrapers

    def getSolutionInstance(self, instans) -> list:
        solution_instances = []
        for item in instans:
            si = SolutionInstance()
            si.name = item
            si.namespace_api = self.connect.resources.get(api_version='v1', kind='Namespace').get()#label_selector=f'discovery.cli.io/si={item}' if item else ''
            si.namespace = [si.namespace_api.items[id] for id, ns in enumerate(si.namespace_api.items) if ns.status.phase == "Active" and ns.metadata.labels['discovery.cli.io/type'] in self.scrapers and si.name in eval(ns.metadata.annotations['discovery.cli.io/si'])]
            #for id, ns in enumerate(si.namespace_api.items):
            #    if ns.metadata.labels['discovery.cli.io/type'] is None or ns.metadata.labels['discovery.cli.io/type'] not in self.scrapers:
            #        #logging.info(f"No scrape for type {ns.metadata.labels['discovery.cli.io/type']}")
            #        del si.namespace_api.items[id]
            solution_instances.append(si)
        return solution_instances
    
class SolutionInstance():
    def __init__(self) -> None:
        self.namespace_api=''
        self.name = ''
        self.namespace = []

    def getAllNamespaces(self) -> list:
        namespaces = []
        for ns in self.namespace:
            namespace = Namespace()
            namespace.ns_name = ns.metadata.name
            namespace.type = ns.metadata.labels['discovery.cli.io/type']
            namespace.subtype = ns.metadata.labels['discovery.cli.io/subtype'] if 'discovery.cli.io/subtype' in ns.metadata.labels.keys() else None
            namespace.level = ns.metadata.labels['discovery.cli.io/level']
            namespace.si = eval(ns.metadata.annotations['discovery.cli.io/si'])
            namespace.parent = eval(ns.metadata.annotations['discovery.cli.io/parent']) if 'annotations' in ns.metadata.keys() and 'discovery.cli.io/parent' in ns.metadata.annotations.keys() else None
            namespaces.append(namespace)
        return namespaces
    
    def getInfraNamespace(self) -> list:
        namespaces = []
        for ns in self.namespace_api.items:
            if ns.metadata.labels['discovery.cli.io/level'] == "infra":
                namespace = Namespace()
                namespace.ns_name = ns.metadata.name
                namespace.type = ns.metadata.labels['discovery.cli.io/type']
                namespace.subtype = ns.metadata.labels['discovery.cli.io/subtype'] if 'discovery.cli.io/subtype' in ns.metadata.labels.keys() else None
                namespace.level = ns.metadata.labels['discovery.cli.io/level']
                namespace.si = eval(ns.metadata.annotations['discovery.cli.io/si'])
                namespace.parent = eval(ns.metadata.annotations['discovery.cli.io/parent']) if 'annotations' in ns.metadata.keys() and 'discovery.cli.io/parent' in ns.metadata.annotations.keys() else None
                namespaces.append(namespace)
        return namespaces
    
    def getAppNamespaces(self) -> list:
        namespaces = []
        for ns in self.namespace_api.items:
            if ns.metadata.labels['discovery.cli.io/level'] == "apps":
                namespace = Namespace()
                namespace.ns_name = ns.metadata.name
                namespace.type = ns.metadata.labels['discovery.cli.io/type']
                namespace.subtype = ns.metadata.labels['discovery.cli.io/subtype'] if 'discovery.cli.io/subtype' in ns.metadata.labels.keys() else None
                namespace.level = ns.metadata.labels['discovery.cli.io/level']
                namespace.si = eval(ns.metadata.annotations['discovery.cli.io/si'])
                namespace.parent = eval(ns.metadata.annotations['discovery.cli.io/parent']) if 'annotations' in ns.metadata.keys() and 'discovery.cli.io/parent' in ns.metadata.annotations.keys() else None
                namespaces.append(namespace)
        return namespaces 
    
    def getProviderNamespaces(self) -> list:
        provider_namespaces = []
        for ns in self.namespace_api.items:
            if ns.metadata.labels['discovery.cli.io/type'] == "provider":
                provider_namespaces.append(ns)
        if len(provider_namespaces) == 0:
            logging.error("Error: No namespaces with 'discovery.cli.io/type' = 'provider' found.")
            sys.exit() 
        if len(provider_namespaces) > 1:
            logging.error("Error: More than one namespace with 'discovery.cli.io/type' = 'provider' found.")
            sys.exit()
        if len(provider_namespaces) == 1:
            ns = provider_namespaces[0]
            logging.info("Info: Namespace with 'discovery.cli.io/type' = 'provider' found in %s", ns.metadata.name)
            namespace = Namespace()
            namespace.ns_name = ns.metadata.name
            namespace.type = ns.metadata.labels['discovery.cli.io/type']
            namespace.subtype = ns.metadata.labels['discovery.cli.io/subtype'] if 'discovery.cli.io/subtype' in ns.metadata.labels.keys() else None
            namespace.level = ns.metadata.labels['discovery.cli.io/level']
            namespace.si = eval(ns.metadata.annotations['discovery.cli.io/si'])
            namespace.parent = eval(ns.metadata.annotations['discovery.cli.io/parent']) if 'annotations' in ns.metadata.keys() and 'discovery.cli.io/parent' in ns.metadata.annotations.keys() else None
            return namespace 

class Namespace():
    def __init__(self) -> None:
        self.ns_name = ''
        self.type = ''
        self.subtype = ''
        self.level = ''
        self.si = ''
        self.parent = []
        self.phase = ''
