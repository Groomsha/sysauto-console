#!/usr/bin/env python3
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

import sys
import json
import argparse
from typing import List, Dict

import sources

help_parser = argparse.ArgumentParser(description="Backup and Restore Virtual Machines and Folders")
help_parser.add_argument("-settings_name_json", type=str, default="settings.json", help="Example: settings.json")

args_parser = help_parser.parse_args()
settings_json = args_parser.setings_name_json


def init_backup(args: List) -> None:
    if args[0] == 1:
        delete_backup = sources.DeleteFolderBackup(args[1], args[2], args[4], args[8])
        delete_backup.main_setup()

        backup_vm_lvm = sources.BackupKVMinLVM(args[1], args[3], args[4], args[2], args[7], args[6])
        backup_vm_lvm.main_setup()
    elif args[0] == 2:
        delete_backup = sources.DeleteFolderBackup(args[1], args[2], args[4], args[8])
        delete_backup.main_setup()

        backup_vm_img = sources.BackupKVMinIMG(args[1], args[3], args[4], args[2], args[6])
        backup_vm_img.main_setup()
    elif args[0] == 3:
        backup_vm_lvm = sources.RestoreKVMinLVM(args[1], args[2], args[5])
        backup_vm_lvm.main_setup()
    elif args[0] == 4:
        backup_vm_img = sources.RestoreKVMinIMG(args[1], args[2], args[5])
        backup_vm_img.main_setup()
    elif args[0] == 5:
        backup_dir_ssh = sources.BackupDirSSH()
        backup_dir_ssh.main_setup()


def close_backup() -> None:
    sys.exit()


if __name__ == '__main__':
    with open(f"{settings_json}", "r") as j:
        settings_json: Dict = json.load(j)

    settings: List = [parameter for _, parameter in settings_json.items()]

    init_backup(settings)
    close_backup()
