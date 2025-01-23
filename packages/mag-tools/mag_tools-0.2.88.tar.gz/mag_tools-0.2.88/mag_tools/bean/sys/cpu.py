import re
import subprocess
from dataclasses import dataclass
from typing import Optional

import wmi

from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.model.cpu_series import CpuSeries

@dataclass
class Cpu:
    serial_number: Optional[int] = None            # 序列号
    name: Optional[str] = None            # 名称
    cpu_type: Optional[str] = None        # CPU类型
    cpu_series: Optional[CpuSeries] = None # CPU系列
    cores: Optional[int] = None           # 核心数量
    performance_cores: Optional[int] = None # 性能核心数量，可选
    efficiency_cores: Optional[int] = None # 能效核心数量，可选
    threads: Optional[int] = None         # 线程数量，可选
    base_clock: Optional[float] = None    # 基础频率（单位：GHz），可选
    boost_clock: Optional[float] = None   # 最大睿频（单位：GHz），可选
    cache: Optional[int] = None           # 缓存大小（单位：MB），可选
    tdp: Optional[int] = None             # 热设计功耗（单位：W），可选
    process: Optional[int] = None         # 制造工艺（单位：nm），可选
    architecture: Optional[str] = None    # 架构类型，可选
    model: Optional[str] = None           # 型号

    @classmethod
    def get_info(cls):
        """
        获取当前系统的CPU信息，并返回一个Cpu实例
        """
        if OperateSystem.is_windows():
            return cls.__get_from_windows()
        elif OperateSystem.is_linux():
            return cls.__get_from_linux()

    @classmethod
    def __get_from_windows(cls):
        """
        从 Windows 系统获取 CPU 信息
        """
        c = wmi.WMI()
        cpu_info = c.Win32_Processor()[0]

        cpu_series, model = cls.__parse_brand_raw(cpu_info.Name.strip())

        return cls(
            serial_number=cpu_info.ProcessorId.strip(),
            name=cpu_info.Name.strip(),
            cpu_type=cpu_info.ProcessorType,
            cpu_series=cpu_series,
            base_clock=float(cpu_info.MaxClockSpeed) / 1000,  # 转换为 GHz
            boost_clock=float(cpu_info.MaxClockSpeed) / 1000,  # 转换为 GHz
            cores=cpu_info.NumberOfCores,
            performance_cores=cpu_info.NumberOfCores,  # 假设性能核心数等于核心数
            efficiency_cores=cpu_info.ThreadCount - cpu_info.NumberOfCores,  # 假设效率核心数等于线程数减去核心数
            threads=cpu_info.ThreadCount,
            architecture=cpu_info.Architecture,
            cache=cpu_info.L2CacheSize,
            model=model,
        )

    @classmethod
    def __get_from_linux(cls):
        """
        从 Linux 系统获取 CPU 信息
        """
        try:
            result = subprocess.run(["lscpu"], capture_output=True, text=True, check=True)
            info = {}
            for line in result.stdout.split("\n"):
                if "Model name:" in line:
                    info["name"] = line.split(":")[1].strip()
                elif "Architecture:" in line:
                    info["architecture"] = line.split(":")[1].strip()
                elif "CPU(s):" in line:
                    info["threads"] = int(line.split(":")[1].strip())
                elif "Core(s) per socket:" in line:
                    info["cores"] = int(line.split(":")[1].strip())
                elif "CPU MHz:" in line:
                    info["base_clock"] = float(line.split(":")[1].strip()) / 1000  # 转换为 GHz
                elif "BogoMIPS:" in line:
                    info["boost_clock"] = float(line.split(":")[1].strip()) / 1000  # 转换为 GHz
                elif "L2 cache:" in line:
                    info["cache"] = int(line.split(":")[1].strip().replace("K", ""))  # 转换为 KB
                elif "Vendor ID:" in line:
                    info["cpu_type"] = line.split(":")[1].strip()
                elif "Model:" in line:
                    info["model"] = line.split(":")[1].strip()

            cpu_series, model = cls.__parse_brand_raw(info.get("name"))

            return cls(
                serial_number=None,  # Linux 系统中可能无法直接获取 CPU 序列号
                name=info.get("name"),
                cpu_type=info.get("cpu_type"),
                cpu_series=cpu_series,
                base_clock=info.get("base_clock"),
                boost_clock=info.get("boost_clock"),
                cores=info.get("cores"),
                performance_cores=info.get("cores"),  # 假设性能核心数等于核心数
                efficiency_cores=info.get("threads") - info.get("cores"),  # 假设效率核心数等于线程数减去核心数
                threads=info.get("threads"),
                architecture=info.get("architecture"),
                cache=info.get("cache"),
                model=model,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error getting CPU information: {e}")
            return cls()

    def __str__(self):
        """
        返回CPU参数的字符串表示
        """
        attributes = [f"Type: {self.cpu_type}"]
        attributes += [f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}" for attr in vars(self) if getattr(self, attr) is not None and attr not in ['id', 'model']]
        return ", ".join(attributes)

    @classmethod
    def __parse_brand_raw(cls, brand_raw: Optional[str] = None):
        """
        从字符串中提取CPU参数并创建CPUParameters实例
        """
        pattern = r"(?P<generation>\d+th Gen) (?P<brand>Intel\(R\) Core\(TM\)) (?P<series>i\d)-(?P<model>\d+K)"

        match = re.match(pattern, brand_raw)
        if match:
            cpu_series = CpuSeries.of_code(match.group('series'))
            model = match.group("model")
            return cpu_series, model
        return None, None

if __name__ == '__main__':
    cpu = Cpu.get_info()
    print(cpu)
