import re
import subprocess
from dataclasses import dataclass, field
from typing import List, Optional

import psutil
import wmi

from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.model.memory_type import MemoryType

@dataclass
class MemoryModule:
    memory_type: Optional[MemoryType] = None
    capacity: Optional[int] = None
    frequency: Optional[int] = None
    voltage: Optional[float] = None
    form_factor: Optional[str] = None
    used_slots: Optional[int] = None
    speed: Optional[int] = None
    latency: Optional[int] = None

    @classmethod
    def get_modules(cls):
        if OperateSystem.is_windows():
            return cls.__get_from_windows()
        else:
            return cls.__get_from_linux()

    def __str__(self):
        """
        返回内存条的字符串表示
        """
        return f"MemoryModule(memory_type='{self.memory_type}', capacity={self.capacity} GB, frequency={self.frequency} MHz, voltage={self.voltage} V, latency={self.latency} CL, speed={self.speed} MB/s, form_factor='{self.form_factor}', used_slots={self.used_slots})"


    @classmethod
    def __get_from_windows(cls):
        modules = []
        c = wmi.WMI()
        for memory in c.Win32_PhysicalMemory():
            memory_type = MemoryType.of_code(memory.MemoryType)
            capacity = int(memory.Capacity) // (1024 ** 3)  # 将字节转换为GB
            frequency = memory.Speed
            voltage = memory.ConfiguredVoltage / 1000.0  # 将毫伏转换为伏特
            form_factor = memory.FormFactor

            modules.append(cls(memory_type=memory_type, capacity=capacity, frequency=frequency, voltage=voltage,
                          form_factor=form_factor))

        return modules

    @classmethod
    def __get_from_linux(cls):
        """
        获取当前系统的所有内存条信息，并返回一个包含多个Memory实例的列表
        """
        result = subprocess.run(['sudo', 'dmidecode', '--type', 'memory'], stdout=subprocess.PIPE)
        output = result.stdout.decode()

        modules = []
        for section in output.split('\n\n'):
            memory_type = capacity = frequency = voltage = form_factor = None

            for line in section.split('\n'):
                if 'Type:' in line and 'Type Detail:' not in line:
                    memory_type = line.split(':')[-1].strip()
                elif 'Size:' in line and 'No Module Installed' not in line:
                    capacity = int(re.findall(r'\d+', line.split(':')[-1].strip())[0])
                elif 'Speed:' in line:
                    frequency = int(re.findall(r'\d+', line.split(':')[-1].strip())[0])
                elif 'Voltage:' in line:
                    voltage = float(re.findall(r'\d+\.\d+', line.split(':')[-1].strip())[0])
                elif 'Form Factor:' in line:
                    form_factor = line.split(':')[-1].strip()

            if memory_type and capacity:
                modules.append(MemoryModule(memory_type=memory_type, capacity=capacity, frequency=frequency, voltage=voltage,
                                            form_factor=form_factor))

        return modules


@dataclass
class Memory:
    """
    内存参数类
    """
    total_capacity: Optional[int] = None
    available_capacity: Optional[int] = None
    used_capacity: Optional[int] = None
    free_capacity: Optional[int] = None
    cache: Optional[int] = None
    buffer_size: Optional[int] = None
    modules: List[MemoryModule] = field(default_factory=list)

    @classmethod
    def get_info(cls):
        """
        获取当前系统的内存信息，并返回一个Memory实例
        """
        # 使用psutil获取内存使用情况
        memory_info = psutil.virtual_memory()
        modules = MemoryModule.get_modules()

        return Memory(
            total_capacity=memory_info.total // (1024 ** 3),  # 将字节转换为GB
            available_capacity=memory_info.available // (1024 ** 3),  # 将字节转换为GB
            used_capacity=memory_info.used // (1024 ** 3),  # 将字节转换为GB
            free_capacity=memory_info.free // (1024 ** 3),  # 将字节转换为GB
            modules=modules
        )

    def __str__(self):
        """
        返回内存参数的字符串表示
        """
        module_info = "\n".join(str(module) for module in self.modules)
        return (f"Memory(total_capacity={self.total_capacity} GB, available_capacity={self.available_capacity} GB, " 
                f"used_capacity={self.used_capacity} GB, free_capacity={self.free_capacity} GB, " 
                f"cache={self.cache} MB, buffer_size={self.buffer_size} MB)\nModules:\n{module_info}")