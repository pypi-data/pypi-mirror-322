import os
import sys
import atexit
import types
import re
import asyncio

from rich import inspect

from . import empty
from . import pluginLoading
from . import config as fileMappingConfig
from . import string


def pathConversion(cpath: os.path, path: os.path) -> os.path:
    """
    当要转化的文件目录在调用文件的临旁时,则可以用这个快速转化

    例：
    |--->
        |-> plugIns
        |-> x.py

    其中x.py要调用plugIns文件夹时即可快速调用

    pathConversion(__file__, "plugIns")
    :param cpath: __file__
    :param path: 必须为文件夹
    :return:
    """
    return os.path.join(os.path.dirname(cpath)if os.path.isfile(cpath)else cpath, os.path.abspath(path))


def configConvertTodict(config) -> dict:
    """
    将配置文件转换为dict格式
    :param config: 配置文件
    :return: dict 格式的配置文件
    """
    # config_type_tuple -> (dict, list, tuple)
    if isinstance(config, fileMappingConfig.config_type_tuple):
        return config
    
    systemConfiguration = {}
    for obj in dir(config) if not isinstance(config, fileMappingConfig.config_type_tuple) else config:
        if obj.startswith("__"):
            continue

        if isinstance(getattr(config, obj), fileMappingConfig.config_type_tuple) if not isinstance(config, fileMappingConfig.config_type_tuple) else isinstance(config[obj], fileMappingConfig.config_type_tuple):
            systemConfiguration[obj] = configConvertTodict(getattr(config, obj))

        else:
            if not obj in dir(empty.empty):
                systemConfiguration[obj] = getattr(config, obj) if not isinstance(config, fileMappingConfig.config_type_tuple) else config[obj]

    return systemConfiguration

@atexit.register
def end():
    """
    结束插件运行
    :return:
    """
    if not fileMappingConfig.endTheTask:
        return

    for key, value in File.invoke.items():
        if fileMappingConfig.functionsName["__end__"] in dir(value):
            name = getattr(value, fileMappingConfig.functionsName["__end__"])
            if isinstance(name, types.FunctionType):
                try:
                    name()

                except fileMappingConfig.error_list_a2 as e:
                    string.endFailed(key, e)

                continue

            if not name in dir(value):
                string.endfunctionNotFound(key, name)
                continue

            pointer = getattr(value, name)
            try:
                pointer()
                continue

            except fileMappingConfig.error_list_a2 as e:
                string.endFailed(key, e)


class fileMapping_dict(dict):
    # 用于包装字典
    # 可以通过 . 访问属性
    def __getattr__(self, item):
        if item in self:
            return self.get(item)

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")


class File:
    """
    callObject
        - 调用对象
    invoke
        - 内行参数
    returnValue
        - 返回参数
    public
        - 公共
    """
    callObject = fileMapping_dict({})
    invoke = fileMapping_dict({})
    returnValue = fileMapping_dict({})
    public = fileMapping_dict({})
    path = None

    def __init__(self,
                 absolutePath: os.path,
                 screening=None,
                 config: dict = None,
                 printLog: bool =False,
                 printPosition=sys.stdout
        ):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件
        :param config: 配置文件 它将会被映射到 public['config']
        :param printLog: 是否打印日志
        :param printPosition: 日志输出位置 默认为 sys.stdout 在终端输出
        """
        if screening is None:
            screening = ["py"]

        if not ((not os.path.isabs(absolutePath)) or (not os.path.islink(absolutePath))):
            raise FileNotFoundError(f"不是一个有效的绝对路径。: '{absolutePath}'")

        # self
        self.printLog = printLog
        self.printPosition = printPosition
        self.path = absolutePath
        ###
        self.filePath = {}
        self.listOfFiles = {}
        for i in os.listdir(absolutePath):
            path = os.path.join(absolutePath, i)
            if os.path.isfile(path) and i.split('.')[-1] in screening:
                # 包函数
                self.listOfFiles[i.split('.')[0]] = path
                self.filePath[i.split('.')[0]] = path

            elif os.path.isdir(path) and os.path.isfile(os.path.join(path, fileMappingConfig.functionsName["__init__.py"])):
                self.listOfFiles[i.split('.')[0]] = path
                self.filePath[i.split('.')[0]] = os.path.join(path, fileMappingConfig.functionsName["__init__.py"])
        ###

        # 加载配置文件
        if config:
            fileMappingConfig.log['printPosition'] = self.printPosition
            fileMappingConfig.log['printLog'] = self.printLog
            self.public['config'] = config

        run = {}
        for key, path in self.filePath.items():
            with open(path, "r", encoding="utf-8") as f:
                s = '\n'.join([
                    i for i in f if i.startswith(fileMappingConfig.functionsName["__level__"])
                ]).strip()

            try:
                _ = {}
                exec(s, {}, _)
                __level__ = _.get("__level__", fileMappingConfig.functions[
                    fileMappingConfig.functionsName["__level__"]
                ])

            except fileMappingConfig.error_all as e:
                __level__ = fileMappingConfig.functions[
                    fileMappingConfig.functionsName["__level__"]
                ]

            run[__level__] = run.get(__level__, []) + [key]

        self._run = dict(sorted(run.items(), reverse=True))
        for __level__, L in self._run.items():
            for name in L:
                self.callObject[name] = pluginLoading.f(self.listOfFiles[name])
                self.invoke[name] = self.callObject[name].pack

    def __run__(self, name, kwargs):
        """
        运行映射文件
        :return:
        """
        _ =self.returnValue[name] = self.callObject[name].run(**kwargs)
        # self.invoke[name] = self.callObject[name].pack

        if not isinstance(_, fileMappingConfig.error_list_a2):
            string.theRunFileWasSuccessful(name)

        else:
            string.theRunFileFailed(name, _)


    def runAll(self, **kwargs):
        """
        运行所有映射文件
        :return:
        """
        for key, data in self._run.items():
            for i in data:
                if self.callObject[i]:
                    self.__run__(i, kwargs)


    def runOne(self, name: str, **kwargs):
        """
        运行单个映射文件
        :return:
        """
        if self.callObject.get(name, False):
            self.__run__(name, kwargs)

        else:
            string.errorNoFile(name)


    def run(self, name: str = None, **kwargs):
        """
        计划在后续版本移除

        运行映射文件
        :return:
        """
        if name is None:
            for key, data in self.listOfFiles.items():
                if self.callObject[key]:
                    self.__run__(key, kwargs)

        else:
            if self.callObject.get(name, False):
                self.__run__(name, kwargs)

            else:
                string.errorNoFile(name)

