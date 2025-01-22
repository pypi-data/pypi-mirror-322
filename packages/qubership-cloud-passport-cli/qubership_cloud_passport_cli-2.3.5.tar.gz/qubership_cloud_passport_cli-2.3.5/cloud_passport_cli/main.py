import logging
import click
from os import environ, path, makedirs
from yaml import safe_load, safe_dump
from scrapers import ScrapeInfo
from discovery import Discover
from collector import Collector
from templating import TemplateProcessor
from connect import Connect
from utility import decode_sensitive, chek_key, schema_generate_util, connect_options
import urllib3
from diagrams import Diagram, Cluster, Edge
from diagrams.k8s import group, podconfig

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)



@click.group(chain=True)
def cli():
    pass

@cli.command("create")
@connect_options
@click.option('--source-template', '-s', 'source', default='.', show_default=True, type=str, help="Path to the directory with cloud passport templates")
@click.option('--dst-dir', '-d', 'directory', default='.', show_default=True, type=str, help="Path to destination directory with render cloud passport")
@click.option('--instance', '-i', 'instance', required=True, type=str, help="Solution instance name")
@click.option('--schema-generate', '-g', 'schema_generate', default=False, show_default=True, type=bool, help="Disable/enable solution instance diagram generation")
@click.option('--secret-key', '-k', 'secret_key', default = environ.get('SECRET_KEY', ''), callback=chek_key, help="Secret key for encrypting sensitive data (file path or environment variable SECRET_KEY)")
@click.option('--visual', '-vi', 'visual', default=False, show_default=True, type=bool, help="Creating a visualization from a solution instance diagram")
def create(kubeconfig, api_token, api_token_prefix, host, verify_ssl, source, directory, instance, secret_key, schema_generate, visual):
    instance = instance.split(',')
    cloud_shema = {}
    connect = Connect(kubeconfig, api_token_prefix, api_token, host, verify_ssl)
    client = connect.client
    scrape = ScrapeInfo(client, secret_key)
    discover = Discover(client, scrape.scrapers.keys())
    instance = discover.getSolutionInstance(instance)
    logging.info(f'Found {len(instance)} solution instances')
    for si in instance:
        collector = Collector()
        templating = TemplateProcessor(f'{source}/template_{si.name}.yaml', collector)
        all_ns = si.getAllNamespaces()
        provider_ns = si.getProviderNamespaces()
        provider_token = scrape.get_scrape('provider_connect', provider_ns.ns_name)

        cloud_shema[si.name] = {}
        cloud_shema[si.name]['infra']= {}
        cloud_shema[si.name]['apps']= {}
        cloud_shema[si.name]['external'] = {}
        if kubeconfig:
            kubeconfig_data = scrape.get_scrape('kubeconfig', kubeconfig)
            collector.add_data("cloud", '', scrape.get_scrape('kubeconfig', kubeconfig))
            connect.api_key = provider_token
            connect.host = f"{kubeconfig_data.data['protocol']}://{kubeconfig_data.data['api_host']}:{kubeconfig_data.data['api_port']}"
            scrape.connect = connect.connect_token()
        
        with click.progressbar(all_ns, label=f"Collecting from solution instances {si.name}") as bar_all_ns:
            for ns in bar_all_ns:
                collector.add_data(ns.type, ns.subtype, scrape.get_scrape(ns.type, ns.ns_name))
                schema_generate_util(schema_generate, cloud_shema, ns, si, collector)
        templating.dump_sensitive(collector, directory, si.name)
        templating.template_passport(collector, directory, si.name)

    if schema_generate:
        if not path.isdir(directory):
            makedirs(directory)
        with open(f'{directory}/cluster_schema.yaml', mode="w") as outfile:
            safe_dump(cloud_shema, outfile)
        if visual:
            visual_diagram.callback(f'{directory}/cluster_schema.yaml')
    logging.info('Successful')

@cli.command("visual_diagram")
@click.option('--schema', '-s', 'schema_path', type=click.Path(exists=True), help="Path to file with solution instance diagram")
def visual_diagram(schema_path):
    with open(schema_path, mode="r", encoding="utf-8") as schema:
        schema_date = safe_load(schema)
    with Diagram(f"cluster Diagram for {list(schema_date.keys())[0]}", show=False, direction='LR', filename=f"{path.dirname(schema_path)}/cluster_diagram"):
        for cloud in schema_date:
            servise = {}
            with Cluster(cloud):
                for level in schema_date[cloud]:
                    with Cluster(level):
                        servise[level] = []
                        for instance in schema_date[cloud][level]:
                            if 'parent' in schema_date[cloud][level][instance].keys():
                                ns = group.NS(instance) if level=='external' else podconfig.CM(instance)
                                servise[level].append(ns)
                                for app in  servise['apps']:
                                    for parent in schema_date[cloud][level][instance]['parent']:
                                        if app.label == parent:
                                            app  >> ns
                            else:
                                servise[level].append(group.NS(instance))
                    if level != 'external':
                        for id, item in enumerate(servise[level]):
                            if id < len(servise[level])-1:
                                item >> Edge(style="invis") >> servise[level][id+1]
                if 'external' in servise.keys() and servise['external']:
                    servise['infra'][-1] >>Edge(style="invis") >> servise['external'][-1]

@cli.command("put_label")
@click.option('--setting', '-s', 'setting', type=click.Path(exists=True), help="Path to schema solution instance file")
@connect_options
def put_label(setting, kubeconfig, api_token_prefix, api_token, host, verify_ssl):
    connect = Connect(kubeconfig, api_token_prefix, api_token, host, verify_ssl)
    client = connect.client
    with open(setting, mode="r", encoding="utf-8") as schema:
        date = safe_load(schema)
    with click.progressbar(date, label=f"Put labels") as bar_date:
        for si in bar_date:
            for level in date[si]:
                for ns in date[si][level]:
                    namespace_api = client.resources.get(api_version='v1', kind='Namespace').get(field_selector=f'metadata.name={ns}')
                    if not namespace_api.items:
                        logging.info(f"Namespace {ns} not found")
                        continue
                    if 'annotations' not in namespace_api.items[0].metadata.keys() or 'discovery.cli.io/si' not in namespace_api.items[0].metadata.annotations.keys():
                        annotation_si = [si]
                    elif si not in namespace_api.items[0].metadata.annotations['discovery.cli.io/si']:
                        annotation_si = []
                        for inst in eval(f"{namespace_api.items[0].metadata.annotations['discovery.cli.io/si']}"):
                            annotation_si.append(inst)
                        annotation_si.append(si)
                    else:
                        annotation_si = namespace_api.items[0].metadata.annotations['discovery.cli.io/si']
                    annotation_parent = str(date[si][level][ns]['parent']) if 'parent' in date[si][level][ns].keys() else None

                    annotations = {"discovery.cli.io/si": str(annotation_si),
                                   "discovery.cli.io/parent": str(date[si][level][ns]['parent']) if 'parent' in date[si][level][ns].keys() else None
                                   } if annotation_parent else {"discovery.cli.io/si": str(annotation_si)}

                    metadata = {'metadata': 
                                {"labels": 
                                    {"discovery.cli.io/level": level,
                                     "discovery.cli.io/type": date[si][level][ns]['type'],
                                     "discovery.cli.io/subtype": date[si][level][ns]['subtype'] if 'subtype' in date[si][level][ns].keys() else None
                                     },
                                "annotations": annotations
                                 }}
                    client.resources.get(api_version='v1', kind='Namespace').patch(body=metadata, name=ns, namespace=ns)
    logging.info('Successful')

@cli.command("decode_sensitive")
#@click.option('--pasport', '-p', 'pasport', type=click.Path(exists=True))
@click.option('--pasport-sensitive', '-s', 'pasport_sensitive', type=click.Path(exists=True))
@click.option('--secret-key', '-k', 'secret_key', default = environ.get('SECRET_KEY', ''), callback=chek_key, help="Secret key for encrypting sensitive data (file path or environment variable SECRET_KEY)")
def upload_pasport(pasport_sensitive, secret_key):
    with open(pasport_sensitive, mode="r", encoding="utf-8") as sensitive:
        sensitive_date = safe_load(sensitive)
    decode_sensitive(secret_key, sensitive_date)
    logging.info(sensitive_date) 

if __name__ == '__main__':
    cli()
