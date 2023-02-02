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
Version: 1.0

Description: Backup and restore script KVM VM

Ihor Cheberiak (c) 2021
https://www.linkedin.com/in/ihor-cheberiak/
"""

import os
import time
from typing import List


class MessengerApplication:
	def __init__(self, dir_logs: str, name_obj: str) -> None:
		self.directory: str = dir_logs
		self.object: str = name_obj

	def logs_creation(self, messages: List) -> None:
		if os.path.isfile(f"{self.directory}{self.object}.log"):
			access_type = "a"
		else:
			access_type = "w"

		time_message: time = time.ctime()
		with open(f"{self.directory}{self.object}.log", access_type) as log:
			for message in messages:
				log.write(f"\n{time_message} {message}")
