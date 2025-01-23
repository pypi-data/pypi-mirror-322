from dataclasses import dataclass
from typing import List, Optional

import wmi

from mag_tools.model.disk_type import DiskType
from mag_tools.model.fs_type import FsType

@dataclass
class DiskPartition:
    fs_type: Optional[FsType] = None
    mount_point: Optional[str] = None       # 驱动装载点

@dataclass
class Disk:
    """
    磁盘参数类
    """
    serial_number: Optional[str] = None   # 序列号
    disk_type: Optional[DiskType] = None # 磁盘类型
    model: Optional[str] = None
    media_type: Optional[str] = None
    manufacturer: Optional[str] = None
    capacity: Optional[int] = None    # 总容量，单位为G

    @classmethod
    def get_info(cls):
        physical_disks = []
        c = wmi.WMI()
        for disk in c.Win32_DiskDrive():
            manufacturer, dick_type = cls.__parse(disk.Model)

            info = cls(serial_number=disk.DeviceID,
                       disk_type=dick_type,
                       model=disk.Model,
                       capacity=int(disk.Size) / 1000**3,
                       media_type=disk.MediaType,
                       manufacturer=manufacturer)
            physical_disks.append(info)

        return physical_disks

    def __str__(self):
        """
        返回磁盘参数的字符串表示
        """
        attributes = [f"{attr.replace('_', ' ').title()}: {getattr(self, attr)}" for attr in vars(self) if
                      getattr(self, attr) is not None]
        return ", ".join(attributes)

    @classmethod
    def __parse(cls, model):
        items = model.split()
        manufacturer = items[0] if len(items) > 0 else None
        dick_type = DiskType.of_code(items[1]) if len(items) > 1 else None

        return manufacturer, dick_type