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
Version: 1.2

Description: Backup and restore script KVM VM

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import time as time_os
import os as terminal_os
import subprocess as shell
from typing import Optional

import sources as service


class BackupKVMinIMG:
    def __init__(self, name_obj: str, dir_obj: str, dir_backup: str, dir_logs: str, compression: int) -> None:
        self.name_obj: str = name_obj
        self.dir_obj: str = dir_obj
        self.dir_backup: str = dir_backup
        self.compression: str = str(compression)
        self.log_recording = service.MessengerApplication(dir_logs, name_obj)

        self.folder_backup: str = ""
        self.touch_folder: str = ""

    def main_setup(self) -> None:
        self.concatenation_folder()

        self.virsh_command()
        self.archive_creation()

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

    def virsh_command(self, command: Optional = None) -> None:
        """ Остонавливает виртуальную машину (VM) и собирает информацию
            для ее восстановления из Backup по надобности в будущем.
        """
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() == ["running"]:
            self.performance_shell(f"virsh shutdown {self.name_obj}")
        if terminal_os.popen(f"virsh domstate {self.name_obj}").read().split() != ["running"]:
            dir_img_temp: str = self.dir_obj[self.dir_obj.find(".")-1:]

            self.performance_shell(f"virsh dumpxml {self.name_obj} > {self.touch_folder}.xml")
            self.performance_shell(f"virsh domblkinfo {self.name_obj} {self.dir_obj} > {self.touch_folder}-{3}_info && virsh vol-pool {self.dir_obj} >> {self.touch_folder}-{dir_img_temp}_info && echo {self.dir_obj} >> {self.touch_folder}-{dir_img_temp}_info")
        
        self.log_recording.logs_creation([f"Process Virsh: Shutdown VM and creation of auxiliary files {self.name_obj} VM!"])

        if command == "start":
            self.performance_shell(f"virsh start {self.name_obj}")
            self.log_recording.logs_creation([f"Process Virsh: Start VM {self.name_obj} - Running"])

    def archive_creation(self) -> None:
        """ compression: Степень сжатия .gz файла от 1 до 9. Чем выше степень,
            тем больше нужно мощностей процессора и времени на создание архива.
        """
        dir_img: str = self.dir_obj[self.dir_obj.find("."):]

        self.log_recording.logs_creation([f"Process GZIP Disk Image: For disk recovery Virtual Machine {self.name_obj}"])
        self.performance_shell(f"dd if={self.dir_obj} | gzip -kc -{self.compression} > {self.touch_folder}{dir_img}.gz")
        self.virsh_command("start")
