from __future__ import annotations
from cryptography.fernet import Fernet
from utility import encode_sensitive
import logging
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)

class CollectorInfo():
    __slots__ = ('_data', '_data_sensitive', 'key')
    def __init__(self, key:Fernet) -> None:
        self.data = {}
        self.data_sensitive = {}
        self.key = key

    @property 
    def data(self) -> dict:  
        return self._data  
    
    @property 
    def data_sensitive(self)-> dict:
        self._data_sensitive = encode_sensitive(self.key, self._data_sensitive)
        #for key in self._data_sensitive.keys(): 
        #    if isinstance(self._data_sensitive[key], str) and '[encrypted:AES256_Fernet]' not in self._data_sensitive[key] and key != 'type':
        #        self._data_sensitive[key] = f"{'[encrypted:AES256_Fernet]'}{cipher.encrypt(self._data_sensitive[key].encode('utf-8')).decode('utf-8')}"
        #    elif isinstance(self._data_sensitive[key], dict):
        #        for k, v in self._data_sensitive[key].items():
        #            if '[encrypted:AES256_Fernet]' not in v and key != 'type':
        #                self._data_sensitive[key][k] = f"{'[encrypted:AES256_Fernet]'}{cipher.encrypt(v.encode('utf-8')).decode('utf-8')}"
        return self._data_sensitive 

    @data.setter  
    def data(self, value:dict) -> dict:
        self._data = value 
    
    @data_sensitive.setter  
    def data_sensitive(self, value:dict)-> dict:
        self._data_sensitive = value 


class Collector():
    def __init__(self) -> None:
        self.data = {}
        self.data_sensitive = {}

        self.data['collector'] = {}
        self.data_sensitive = {}

    def add_data(self, type:str, subtype:str, collector:CollectorInfo) -> None:
        if subtype and type not in self.data['collector'].keys():
            self.data['collector'][type] = {}
            self.data['collector'][f'{type}-{subtype}'] = collector.data
            #for sicret in collector.data_sensitive:
            self.data_sensitive[f'{type}-{subtype}'] = collector.data_sensitive
        elif subtype and type in self.data['collector'].keys():
            self.data['collector'][type][subtype] = collector.data
            self.data_sensitive[f'{type}-{subtype}'] = collector.data_sensitive
        elif not subtype and type not in self.data['collector'].keys():
            self.data['collector'][type] = collector.data
            self.data_sensitive[f'{type}'] = collector.data_sensitive
        else:
            logging.info(f'type already exists without subtype {type}')