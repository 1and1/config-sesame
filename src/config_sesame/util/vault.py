# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Hashicorp Vault API (based on ``hvac``).
"""
# Copyright ©  2016 1&1 Group <jh@web.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, unicode_literals, print_function

import os
import getpass

import hvac
from rudiments import security


class Connection(object):
    """Hashicorp Vault connection."""

    def __init__(self, url=None, token=None):
        self.url = url or os.environ.get('VAULT_ADDR')  # TODO: also add lookup from config / cmd line
        self.token = token or os.environ.get('VAULT_TOKEN')
        self.user, self.auth_by = getpass.getuser(), 'environment'
        if not self.token:
            access = security.Credentials(self.url)
            self.user, self.token = access.auth_pair()
            self.auth_by = access.source
        self.api = hvac.Client(url=self.url, token=self.token)

    def __str__(self):
        """Return human readable description of this connection."""
        return "Connection to {} [authenticated by {}'s token from {}]".format(
            self.url, self.user, self.auth_by or 'N/A')
