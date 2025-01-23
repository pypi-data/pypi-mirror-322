import re
import subprocess
from dataclasses import dataclass
from typing import Optional

import wmi

from mag_tools.bean.sys.operate_system import OperateSystem
from mag_tools.model.memory_type import MemoryType

@dataclass
class MemoryModule:
    memory_type: Optional[MemoryType] = None  # 内存类型
    capacity: Optional[int] = None            # 容量 (GB)
    frequency: Optional[int] = None           # 频率 (MHz)
    voltage: Optional[float] = None           # 电压 (V)
    form_factor: Optional[str] = None         # 形态
    used_slots: Optional[int] = None          # 使用的插槽数
    speed: Optional[int] = None               # 速度 (MB/s)
    latency: Optional[int] = None             # 延迟 (CL)
    serial_number: Optional[str] = None       # 序列号

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
        return f"MemoryModule(memory_type='{self.memory_type}', capacity={self.capacity} GB, frequency={self.frequency} MHz, voltage={self.voltage} V, latency={self.latency} CL, speed={self.speed} MB/s, form_factor='{self.form_factor}', used_slots={self.used_slots}, serial_number='{self.serial_number}')"

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
            serial_number = memory.SerialNumber

            modules.append(cls(memory_type=memory_type, capacity=capacity, frequency=frequency, voltage=voltage,
                               form_factor=form_factor, serial_number=serial_number))

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
            memory_type = capacity = frequency = voltage = form_factor = serial_number = None

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
                elif 'Serial Number:' in line:
                    serial_number = line.split(':')[-1].strip()

            if memory_type and capacity:
                modules.append(MemoryModule(memory_type=memory_type, capacity=capacity, frequency=frequency, voltage=voltage,
                                            form_factor=form_factor, serial_number=serial_number))

        return modules

# 示例调用
if __name__ == "__main__":
    modules = MemoryModule.get_modules()
    for module in modules:
        print(module)
