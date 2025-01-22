import re
from typing import Optional

import psutil
from cpuinfo import cpuinfo

from mag_tools.model.cpu_type import CpuType


class Cpu:
    def __init__(self, cpu_type: Optional[CpuType] = None, performance_cores: Optional[int] = None, efficiency_cores: Optional[int] = None,
                 threads: Optional[int] = None, base_clock: Optional[float] = None, boost_clock: Optional[float] = None,
                 cache: Optional[int] = None, tdp: Optional[int] = None, process: Optional[int] = None,
                 architecture: Optional[str] = None, model: Optional[str] = None, brand_raw: Optional[str] = None, id_: Optional[int] = None):
        """
        初始化CPU参数类

        :param cpu_type: CPU类型
        :param performance_cores: 性能核心数量，可选
        :param efficiency_cores: 能效核心数量，可选
        :param threads: 线程数量，可选
        :param base_clock: 基础频率（单位：GHz），可选
        :param boost_clock: 最大睿频（单位：GHz），可选
        :param cache: 缓存大小（单位：MB），可选
        :param tdp: 热设计功耗（单位：W），可选
        :param process: 制造工艺（单位：nm），可选
        :param architecture: 架构类型，可选
        :param model: 型号
        :param brand_raw: 品牌
        :param id_: 标识
        """
        self.cpu_type = cpu_type
        self.performance_cores = performance_cores
        self.efficiency_cores = efficiency_cores
        self.threads = threads
        self.base_clock = base_clock
        self.boost_clock = boost_clock
        self.cache = cache
        self.tdp = tdp
        self.process = process
        self.architecture = architecture
        self.model = model
        self.brand_raw = brand_raw
        self.id = id_

        if not self.cpu_type and self.brand_raw:
            self.__parse_brand_raw()

    @classmethod
    def get_info(cls):
        """
        获取当前系统的CPU信息，并返回一个Cpu实例
        """
        cpu_info = cpuinfo.get_cpu_info()
        psutil_cpu_info = psutil.cpu_freq()

        base_clock = psutil_cpu_info.current / 1000  # 将MHz转换为GHz
        boost_clock = psutil_cpu_info.max / 1000  # 将MHz转换为GHz
        threads = psutil.cpu_count(logical=True)
        architecture = cpu_info['arch']
        cache = cpu_info.get('l3_cache_size', None)  # 获取L3缓存大小

        return cls(
            base_clock=base_clock,
            boost_clock=boost_clock,
            threads=threads,
            architecture=architecture,
            cache=cache,
            brand_raw=cpu_info['brand_raw'])

    def __str__(self):
        """
        返回CPU参数的字符串表示
        """
        attributes = [f"Type: {self.cpu_type}"]
        attributes += [f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}" for attr in vars(self) if getattr(self, attr) is not None and attr not in ['id', 'model']]
        return ", ".join(attributes)

    def __parse_brand_raw(self):
        """
        从字符串中提取CPU参数并创建CPUParameters实例
        """
        pattern = r"(?P<generation>\d+th Gen) (?P<brand>Intel\(R\) Core\(TM\)) (?P<series>i\d)-(?P<model>\d+K)"

        match = re.match(pattern, self.brand_raw)
        if match:
            self.cpu_type = CpuType.of_code(match.group('series'))
            self.model = match.group("model")