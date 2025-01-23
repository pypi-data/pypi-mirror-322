# coding=utf-8

import os
from glob import glob

import yaml


def detect_file_full_path(conf_file: str = 'conn.ini'):
    sep = os.sep
    path1 = os.path.abspath('')
    path2 = os.path.abspath(os.path.dirname(os.getcwd()))
    path3 = os.path.abspath(os.path.join(os.getcwd(), '../..'))
    if path1 + sep + conf_file in glob(path1 + sep + '*'):
        target_path = path1 + sep
    elif path2 + sep + conf_file in glob(path2 + sep + '*'):
        target_path = path2 + sep
    elif path3 + sep + conf_file in glob(path3 + sep + '*'):
        target_path = path3 + sep
    else:
        raise FileNotFoundError('cannot locate {}'.format(conf_file, __file__))
    return target_path + conf_file


class Configs(object):
    def __init__(self, conf_file='config.yml'):
        self.config = self.__load_yaml__(conf_file)

        self.dynamic_loading(conf_file, key='strategy.params')
        self.dynamic_loading(conf_file, key='strategy.name')

    def dynamic_loading(self, conf_file, key='strategy.params'):
        l1, l2 = key.split('.')

        if "${" + key + "}" in self.config['strategy']['cls_obj']:
            strategy_params_back = os.environ.get(key, None)

            os.environ[key] = self.config[l1][l2]

            self.config = self.__load_yaml__(conf_file)

            if strategy_params_back is not None:
                os.environ.pop(key)
                os.environ[key] = strategy_params_back

    @staticmethod
    def __load_yaml__(conf_file):
        full_path = detect_file_full_path(conf_file=conf_file)
        with open(full_path, 'r', encoding="utf-8") as f:
            content = f.read()
            # 替换环境变量
            content = os.path.expandvars(content)

            return yaml.load(content, Loader=yaml.FullLoader)

    def __getitem__(self, item):
        return self.config[item]

    def items(self):
        return self.config.items()

    def keys(self):
        return self.config.keys()

    def values(self):
        return self.config.values()


if __name__ == '__main__':
    config = Configs('test_config.yml')

    # os.environ["strategy.params"] = (config.config['strategy']['params'])

    print(1)

    pass
