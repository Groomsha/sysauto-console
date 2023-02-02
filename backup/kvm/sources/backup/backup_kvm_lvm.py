#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""
Project Name: 'backup-kvm'
Version: 1.5

Description: Скрипт позволяет делать автоматические бекапы виртуальных машин 
используя его в CRON для гипервизора KVM размещенных на блочном устройстве LVM.

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import sys
import time as time_os
import os as terminal_os
import subprocess as shell

import sources as service


class BackupKVMinLVM:
    def __init__(self, name_obj: str, dir_obj: str, dir_backup: str, dir_logs: str, size_snap: int, compression: int) -> None:
        self.name_obj: str = name_obj
        self.dir_obj: str = dir_obj
        self.dir_backup: str = dir_backup
        self.size_snap: int = int(size_snap)
        self.compression: str = str(compression)

        self.folder_backup: str = ""
        self.touch_folder: str = ""
        self.log_recording = service.MessengerApplication(dir_logs, name_obj)

    def main_setup(self) -> None:
        self.concatenation_folder()

        self.performance_shell(f"mkdir -p {self.dir_backup}{self.folder_backup}/")
        self.log_recording.logs_creation([f"Start Process Backup Virtual Machine: {self.name_obj} {self.dir_backup}{self.folder_backup}"])
        
        self.virsh_command()
        self.lvm_command("create")
        self.virsh_restore()

        self.log_recording.logs_creation(["#"*120])
    
    def concatenation_folder(self) -> None:
        time_backup: time_os = time_os.strftime("%d.%m.%Y")

        self.folder_backup = f"{self.name_obj}_{time_backup}"
        self.touch_folder = f"{self.dir_backup}{self.folder_backup}/{self.name_obj}"
    
    def performance_shell(self, command, wait_shell: bool = True) -> None:
        shell_os = shell.Popen(command, stdout=shell.PIPE, stderr=shell.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell:
            shell_os.wait()
        
        output, errors = shell_os.communicate()
        if len(str(output)) != 0:
            self.log_recording.logs_creation(str(output.strip()).splitlines())
        if len(str(errors)) != 0:
            self.log_recording.logs_creation(str(errors.strip()).splitlines())
    
    def virsh_command(self) -> None:
        """ Остонавливает виртуальную машину (VM) и собирает информацию
            для ее восстановления из Backup по надобности в будущем.
        """
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() == ["running"]:
            self.performance_shell(f"virsh save {self.name_obj} {self.touch_folder}.vmstate --running")
        if terminal_os.popen(f"fvirsh domstate {self.name_obj}").read().split() != ["running"]:
            self.performance_shell(f"virsh dumpxml {self.name_obj} > {self.touch_folder}.xml")
            self.performance_shell(f"virsh domblkinfo {self.name_obj} {self.dir_obj} > {self.touch_folder}-raw_info && virsh vol-pool {self.dir_obj} >> {self.touch_folder}-raw_info && echo {self.dir_obj} >> {self.touch_folder}-raw_info")
        
        self.log_recording.logs_creation([f"Process Virsh Create: {self.name_obj}.vmstate --running and creation of auxiliary files VM!"])
    
    def lvm_command(self, command: str) -> None:
        """ command: (create) Создать LVM_Snap. (remove) Удалить LVM_Snap.
            ratio: Размер таблицы(буфера), на каждые 8Gb LVM c VM нужно 256M.
            ratio=2 это 512M Snapshot для VM размером меньше чем 16Gb
        """
        if command == "create":
            ratio: str = str(self.size_snap*256)

            self.performance_shell(f"sudo lvcreate -s -n {self.dir_obj}_snap -L{ratio}M {self.dir_obj}")
            self.log_recording.logs_creation([f"LVM Snapshot Create: {self.dir_obj}_snap Size: {ratio}M Target: {self.dir_obj}"])
        elif command == "remove":
            self.performance_shell(f"sudo lvremove -f {self.dir_obj}_snap")
            self.log_recording.logs_creation([f"LVM Snapshot Remove {self.dir_obj}_snap"])
    
    def virsh_restore(self) -> None:
        """ Запускает виртуальную машину (VM) из сохраненного ранее состояния """
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() != ["running"]:
            self.log_recording.logs_creation([f"Start Process Restore Virtual Machine: {self.name_obj}.vmstate --running"])
            self.performance_shell(f"virsh restore {self.touch_folder}.vmstate")
            self.archive_creation()
        else:
            self.log_recording.logs_creation(["Error Process Restore VM: The VM is not turned off, removing the folder with oriental information!"])
            self.performance_shell(f"rm -r {self.dir_backup}{self.folder_backup}/")
            self.lvm_command("remove")
            self.close_backup()

    def archive_creation(self) -> None:
        """ compression: Степень сжатия .gz файла от 1 до 9. Чем выше степень,
            тем больше нужно мощностей процессора и времени на создание архива.
        """
        self.log_recording.logs_creation([f"Process GZIP LVM Snapshot: For disk recovery Virtual Machine {self.name_obj}"])
        self.performance_shell(f"dd if={self.dir_obj}_snap | gzip -ck -{self.compression} > {self.touch_folder}.gz")

        self.log_recording.logs_creation(["Allocated to LVM Snapshot: Allocated should be < 100% for performance Snapshot!"])
        self.performance_shell(f"sudo lvdisplay {self.dir_obj}_snap")

        self.lvm_command("remove")

    def close_backup(self) -> None:
        sys.exit()
