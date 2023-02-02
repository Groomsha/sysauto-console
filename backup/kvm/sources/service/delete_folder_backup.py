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
Version: 1.1

Description: Backup and restore script KVM VM

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import subprocess
from typing import List
from datetime import datetime

import sources as service


class DeleteFolderBackup:
    def __init__(self, name_obj: str, dir_logs: str, dir_backup: str, number_archives: int) -> None:
        self.shell_output: List = []

        self.name_obj: str = name_obj
        self.dir_backup: str = dir_backup
        self.number_archives: int = number_archives
        self.log_recording = service.MessengerApplication(dir_logs, "delete_backup")
    
    def main_setup(self) -> None:
        self.performance_shell(f"ls {self.dir_backup}")

        for rm in self.shell_output[self.number_archives:]:
            self.performance_shell(f"rm -r {self.dir_backup}{rm}")
            self.log_recording.logs_creation([f"rm -r {self.dir_backup}{rm}"])
    
    def performance_shell(self, command: str, wait_shell: bool = True) -> None:
        shell_os = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash", universal_newlines=True)

        if wait_shell:
            shell_os.wait()

        output, errors = shell_os.communicate()

        if shell_os.returncode != 0:
            self.log_recording.logs_creation(str(errors.strip()).splitlines())
        else:
            if command[:2] == "ls":
                for data in str(output.strip()).splitlines():
                    if data[:-11] == self.name_obj:
                        self.shell_output.append(data)

                self.shell_output.sort(key=lambda date: datetime.strptime(date[-10:], "%d.%m.%Y"), reverse=True)
        