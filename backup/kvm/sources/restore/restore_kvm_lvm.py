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

Description: Скрипт позволяет востоновить бекапы виртуальных 
машин для гипервизора KVM размещенных на блочном устройстве LVM.

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import subprocess as shell

import sources as service


class RestoreKVMinLVM:
    def __init__(self, name_obj: str, dir_logs: str, backup_folder: str) -> None:
        self.name_obj: str = name_obj
        self.backup_folder: str = backup_folder
        self.log_recording = service.MessengerApplication(dir_logs, name_obj)

        self.size_lvm_block: str = ""
        self.dev_lvm_block: str = ""
    
    def main_setup(self) -> None:
        with open(f"{self.backup_folder}{self.name_obj}-raw_info") as backup:
            temp_str: str = ""
            for line in backup:
                temp_str += line

        *rest, self.size_lvm_block, _, self.dev_lvm_block = temp_str.split()

        self.log_recording.logs_creation([f"Start Process Restoring Virtual Machine: {self.name_obj} {self.backup_folder}"])

        self.virsh_command("destroy")
        self.lvm_command("remove")
        self.virsh_command("define")
        self.lvm_command("create")

        print("Restore Сompleted!")
    
    def performance_shell(self, command: str, wait_shell: bool = True) -> None:
        shell_os = shell.Popen(command, stdout=shell.PIPE, stderr=shell.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell:
            shell_os.wait()
        
        output, errors = shell_os.communicate()
        if len(str(output)) != 0:
            self.log_recording.logs_creation(str(output.strip()).splitlines())
        if len(str(errors)) != 0:
            self.log_recording.logs_creation(str(errors.strip()).splitlines())
    
    def virsh_command(self, command: str) -> None:
        """ Уничтажает виртуальную машину (VM), восстановление 
            из Backup и запускает виртуальную машину (VM)
        """
        if command == "destroy":
            self.performance_shell(f"virsh destroy {self.name_obj}")
        elif command == "define":
            self.performance_shell(f"virsh define {self.backup_folder}{self.name_obj}.xml")
        elif command == "restore":
            self.performance_shell(f"virsh restore {self.backup_folder}{self.name_obj}.vmstate")
    
    def lvm_command(self, command: str) -> None:
        """ command: (create) Создать блочное устройство LVM. (remove) Удалить блочное устройство LVM.
            size: Размер блочного устройства для Virtual Machine в 'Байтах'. Из файла -raw_info. 
        """

        lvm_size_str: str = str(self.size_lvm_block)
        lvm_split_str: str = self.dev_lvm_block.split('/')[-2]

        if command == "create":
            self.performance_shell(f"sudo lvcreate -y -n {self.name_obj} -L{lvm_size_str}B {lvm_split_str}")
            self.log_recording.logs_creation([f"LVM Block Device Create: {self.name_obj} Size: {lvm_size_str} Byte Target: {self.dev_lvm_block}"])
            self.archive_creation()
        elif command == "remove":
            self.performance_shell(f"sudo lvremove -f {self.dev_lvm_block}")
            self.log_recording.logs_creation([f"LVM Block Device Remove {self.dev_lvm_block}"])
    
    def archive_creation(self) -> None:
        self.log_recording.logs_creation([f"Process GUNZIP LVM Block Device: For disk recovery VM: {self.name_obj}"])
        self.performance_shell(f"gunzip -ck {self.backup_folder}{self.name_obj}.gz > {self.dev_lvm_block}")
        self.virsh_command("restore")
