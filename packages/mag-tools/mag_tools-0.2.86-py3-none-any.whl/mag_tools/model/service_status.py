from mag_tools.model.base_enum import BaseEnum

class CpuType(BaseEnum):
    """
    枚举类表示不同类型的CPU及其固定参数
    """
    INTEL_I3 = ("I3", "Intel Core i3", "Hybrid", 3.6, 4.2, 6, 65, 14)
    INTEL_I5 = ("I5", "Intel Core i5", "Hybrid", 3.7, 4.4, 9, 65, 14)
    INTEL_I7 = ("I7", "Intel Core i7", "Hybrid", 3.8, 4.7, 12, 65, 14)
    INTEL_I9 = ("I9", "Intel Core i9", "Hybrid", 3.9, 5.0, 16, 95, 14)
    AMD_3 = ("R3", "AMD Ryzen 3", "Zen", 3.6, 4.0, 6, 65, 7)
    AMD_5 = ("R5", "AMD Ryzen 5", "Zen", 3.7, 4.2, 8, 65, 7)
    AMD_7 = ("R7", "AMD Ryzen 7", "Zen", 3.8, 4.4, 12, 65, 7)
    AMD_9 = ("R9", "AMD Ryzen 9", "Zen", 3.9, 4.6, 16, 105, 7)

    def __init__(self, code, desc, architecture, base_clock, boost_clock, cache, tdp, process):
        """
        初始化CPU类型枚举类

        :param code: CPU类型的值
        :param desc: CPU类型的描述
        :param architecture: CPU的架构
        :param base_clock: 基础频率（单位：GHz）
        :param boost_clock: 最大睿频（单位：GHz）
        :param cache: 缓存大小（单位：MB）
        :param tdp: 热设计功耗（单位：W）
        :param process: 制造工艺（单位：nm）
        """
        super().__init__(code, desc)
        self.architecture = architecture
        self.base_clock = base_clock
        self.boost_clock = boost_clock
        self.cache = cache
        self.tdp = tdp
        self.process = process

    def __str__(self):
        """
        返回CPU类型的字符串表示

        :return: CPU类型的字符串表示
        """
        return f"CpuType(value='{self.value}', desc='{self.desc}', architecture='{self.architecture}', base_clock={self.base_clock} GHz, boost_clock={self.boost_clock} GHz, cache={self.cache} MB, tdp={self.tdp} W, process={self.process} nm)"