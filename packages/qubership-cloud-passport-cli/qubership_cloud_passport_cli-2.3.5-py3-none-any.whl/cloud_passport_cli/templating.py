from __future__ import annotations
import jinja2
import logging
from os import path, makedirs
from yaml import safe_dump
from ruamel.yaml import YAML
from collector import Collector
from collections import abc
import jmespath
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)

class TemplateHandler():
    def __init__(self, collector: Collector) -> None:
        self.collector = collector

    def secrets(self, value: str) -> str:
        value = value.split('collector.')[1].split('.')
        wrapped_value = [wrap_word(w) for w in value]
        jmespath_data = jmespath.search(".".join(wrapped_value[:len(wrapped_value) - 1]), self.collector.data_sensitive)
        if jmespath_data:
            output = f"{'-'.join(value[:-1])}.{value[-1]}"
            return "{{ secrets('%s') }}" % output.replace('provider-', '')
        else:
            return "\"\""

def straighten_dict(data:dict) -> dict:
    straighten_data = {}
    for k_top, v_top in data.items():
        if 'provider' in k_top or 'collector' in k_top:
            straighten_data.update(straighten_dict(data[k_top]))
        else:
            for k, v in v_top.items():
                print(k_top)

                if k_top == 'cloud-deploy-sa-token':
                    key = k_top
                elif k == 'creds':
                    key = f'{k_top}'
                else:
                    key = f'{k_top}-{k}'

                straighten_data[key] = v
    return straighten_data

def my_finalize(thing):
    return thing if thing is not None else '""'

def to_dict(v, key):
    emp_dict = p_list = {}
    leng = len(key)
    for index, item in enumerate(key):
        p_list[item] = v if index == leng - 1 else {}
        p_list = p_list[item]
    return emp_dict

class SilentUndefined(jinja2.Undefined):
    def _fail_with_undefined_error(self) -> str:
        #logging.info(f'JINJA2: Collector has no information about "{self._undefined_name}"')
        return "Undefined"


class UpdatableDict(dict):
    def __init__(self):
        super().__init__()


    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def update_to_list(self, d, u):
        for k, v in u.items():
            if isinstance(v, abc.Mapping):
                if not k in d:
                    d[k] = []
                d[k] = self.update_to_list(d.get(k, {}), v)
            elif not k in d:
                d.append(f'{k}.{v}')
        return d

    def update_to_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, abc.Mapping):
                d[k] = self.update_to_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

class Template():
    def __init__(self, path_template:str) -> None:
        self.path_template = path_template
        self.base_name_template = path.basename(path_template)
        self.dir_name_template = path.dirname(path_template)
        self.template_all = {}
        self.template_data = self.load()
        self.template_data, self.template_data_secrets = self.load()
        self.revert_data =  {'data':self.revert(self.template_data), 'data_secrets':self.revert(self.template_data_secrets)}

    def clear_jinja2_hooks(self, date_schema, data_secrets, data) -> str:
        for key, value in date_schema.items():
            if isinstance(value, dict):
                data_secrets[key] = {}
                data[key] = {}
                self.clear_jinja2_hooks(value, data_secrets[key], data[key])
            elif isinstance(value, str):
                if value.startswith('<{ secrets'):
                    data_secrets[key] = value.replace("<{ secrets('", '').replace("') }}", '')
                else:
                    data[key] = value.replace('<{ ', '').replace(' }}', '')
        return data, data_secrets

    def load(self):
        yaml = YAML(typ='jinja2')
        with open(self.path_template, mode="r", encoding="utf-8") as schema:
            self.template_all = yaml.load(schema)
        data_secrets = {}
        data = {}
        return self.clear_jinja2_hooks(self.template_all, data_secrets, data)

    def revert(self, data):
        myDict = UpdatableDict()
        [myDict.update_to_list(myDict, {v:{key:k}}) for key in data.keys() for (v,k) in zip(data[key].values(), data[key].keys())]
        return dict(myDict)


def wrap_word(w):
    if '-' in w:
        w = f'"{w}"'
    return w


def clean_empty_data(data_sensitive):
    for key, value in list(data_sensitive.items()):
            if isinstance(value, dict):
                clean_empty_data(value)
                if 1 >= len(value) and 'type' in value:
                    del data_sensitive[key]
            elif '' == value:
                del data_sensitive[key]

class TemplateProcessor():
    def __init__(self, path_template:str, collector:Collector) -> None:
        self.template = Template(path_template)
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template.dir_name_template), undefined=SilentUndefined, finalize=my_finalize)
        handler = TemplateHandler(collector)
        self.environment.globals['secrets'] = handler.secrets

    def template_passport(self, collector:Collector, dest_dir:str, si_name:str) -> None:
        template = self.environment.get_template(self.template.base_name_template)
        content = template.render(collector.data)
        if not path.isdir(dest_dir):
            makedirs(dest_dir)
        with open(f"{dest_dir}/new_passport_{si_name}.yaml", mode="w", encoding="utf-8") as message:
            message.write(content)

    def dump_sensitive(self, collector:Collector, dest_dir:str, si_name:str) -> None:
        if not path.isdir(dest_dir):
            makedirs(dest_dir)
        sub_data_sensitive = UpdatableDict()
        for secret in self.template.revert_data['data_secrets'].keys():
            keys_secret = secret.split(".")
            wrapped_keys_secret = [wrap_word(w) for w in keys_secret]

            clean_empty_data(collector.data_sensitive)
            jmespath_data = jmespath.search(".".join(wrapped_keys_secret[:len(wrapped_keys_secret)-1]), {'collector':collector.data_sensitive})
            if jmespath_data:
                sub_data_sensitive.update_to_dict(sub_data_sensitive, to_dict(jmespath_data, keys_secret[:len(keys_secret)-1]))
            #else:
            #    for secret_in_template in self.template.revert_data['data_secrets'][secret]:
            #        key_value = secret_in_template.split('.')
            #        del  self.template.template_all[key_value[0]][key_value[1]]
            #    yaml = YAML()
            #    with open(self.template.path_template, mode="w+") as outfile:
            #        yaml.dump(self.template.template_all, outfile)
        sub_data_sensitive.update_to_dict(sub_data_sensitive, to_dict(collector.data_sensitive['provider']['cloud-deploy-sa-token']['creds'], ['collector', 'provider', 'cloud-deploy-sa-token', 'creds']))
        data_sensitive = straighten_dict(sub_data_sensitive)
        with open(f'{dest_dir}/data_sensitive_{si_name}.yaml', mode="w+") as outfile:
            safe_dump(data_sensitive, outfile)
