import click
import logging
from cryptography.fernet import Fernet
from os import getenv, path
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)

class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            ex_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with '
                ' arguments: [' + ex_str + '].'
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    ', '.join(self.mutually_exclusive)
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

def connect_options(function):
    function = click.option('--config', '-c', 'kubeconfig', type=click.Path(), help="Path to kubeconfig file", cls=MutuallyExclusiveOption, mutually_exclusive=["api_token", "api_token_prefix", "host", "verify_ssl"])(function)
    function = click.option('--api-token', '-t', 'api_token', type=str, help="Api key string", cls=MutuallyExclusiveOption, mutually_exclusive=["kubeconfig"])(function)
    function = click.option('--token-prefix', '-p', 'api_token_prefix', default="Bearer", show_default=True, type=str, help="API key prefix", cls=MutuallyExclusiveOption, mutually_exclusive=["kubeconfig"])(function)
    function = click.option('--host', '-h', 'host', type=str, help="IP kubernetes host", cls=MutuallyExclusiveOption, mutually_exclusive=["kubeconfig"])(function)
    function = click.option('--verify-ssl', '-vs', 'verify_ssl', default=False, show_default=True, type=bool, help="Disable/enable SSL verification", cls=MutuallyExclusiveOption, mutually_exclusive=["kubeconfig"])(function)
    return function

def chek_key(ctx:click.Context, param:click.Parameter, value:str):
    if path.exists(value):
        with open(f"{value}", mode="r", encoding="utf-8") as message:
            value = message.read()
        return value
    elif getenv('SECRET_KEY'):
        return value
    elif click.confirm('env variable SECRET_KEY is empty or secret_key is not a file \ngenerate automatically key file?', abort=True):
        #logging.info('secret_key automatically generated in key file')
        secret_key = Fernet.generate_key()
        with open('key', mode="wb") as key_file:
            key_file.write(secret_key)
        return secret_key
        
def decode_sensitive(secret_key:str, sensitive_data) -> str:
    cipher = Fernet(secret_key)
    for key, data in sensitive_data.items():
        if isinstance(data, dict):
            decode_sensitive(secret_key, data)
        elif '[encrypted:AES256_Fernet]' in data:
            sensitive_data[key] = cipher.decrypt(data.replace('[encrypted:AES256_Fernet]', '').encode('utf-8')).decode('utf-8') 
    return sensitive_data

def encode_sensitive(secret_key:str, sensitive_data) -> str:
    cipher = Fernet(secret_key)
    for key, data in sensitive_data.items():
        if isinstance(data, dict):
            encode_sensitive(secret_key, data)
        elif '[encrypted:AES256_Fernet]' not in data and key != 'type' and data != '':
            sensitive_data[key] = f"{'[encrypted:AES256_Fernet]'}{cipher.encrypt(data.encode('utf-8')).decode('utf-8')}"
    return sensitive_data


def schema_generate_util(schema_generate, cloud_shema, ns, si, collector):
    if schema_generate:
        cloud_shema[si.name][ns.level][ns.ns_name] = {"type": ns.type}
        if ns.subtype:
            cloud_shema[si.name][ns.level][ns.ns_name].update({"subtype":ns.subtype})
        if ns.parent:
            cloud_shema[si.name][ns.level][ns.ns_name].update({"parent":ns.parent})
        if ns.type == "provider":
            for external in collector.data['collector']['provider']:
                cloud_shema[si.name]['external'][external] = {"type": 'external'}
                cloud_shema[si.name]['external'][external].update({"subtype": external})
                cloud_shema[si.name]['external'][external].update({"parent": [ns.ns_name]})
