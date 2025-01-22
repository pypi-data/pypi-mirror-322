from __future__ import annotations
from os import path
from kubernetes import client, config, dynamic

class Connect():
    #isinstance = None

    def __new__(cls, kubeconfig:str, api_key_prefix:str, api_key:str, host:str, verify_ssl:bool) -> Connect:
        Connect.isinstance = super().__new__(cls)
        Connect.kubeconfig = kubeconfig
        Connect.api_key = api_key
        Connect.api_key_prefix = api_key_prefix
        Connect.host = host
        Connect.verify_ssl = verify_ssl
        Connect.client = Connect.connect_kubeconfig(Connect) if kubeconfig and path.exists(kubeconfig) else Connect.connect_token(Connect)
        return Connect.isinstance
        
    def connect_token(self) -> Connect:
        configuration = client.Configuration()
        configuration.api_key['authorization'] = self.api_key
        configuration.api_key_prefix['authorization'] = self.api_key_prefix
        configuration.host = self.host
        configuration.verify_ssl = self.verify_ssl
        return dynamic.DynamicClient(client.ApiClient(configuration))
    
    def connect_kubeconfig(self) -> Connect:
        config.load_kube_config(config_file=self.kubeconfig)
        return dynamic.DynamicClient(client.ApiClient())