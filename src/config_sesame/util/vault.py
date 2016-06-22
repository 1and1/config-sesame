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

import io
import os
import getpass

import hvac
from rudiments import security

from .._compat import urljoin

VAULT_TOKEN_FILE = '~/.vault-token'


def default_credentials(url=None, token=None):
    """Return default credentials from env / configuration in a tuple (url, user, token, auth_by)."""
    url = url or os.environ.get('VAULT_ADDR')  # TODO: also add lookup from config / cmd line
    token = token or os.environ.get('VAULT_TOKEN')
    user, auth_by = getpass.getuser(), 'environment'

    token_file = os.path.expanduser(VAULT_TOKEN_FILE)
    if not token and os.path.exists(token_file):
        with io.open(token_file, encoding='utf-8') as handle:
            token = handle.readline().strip()
            auth_by = 'vault-token-file'

    return (url, user, token, auth_by)


def get_credentials(url=None, token=None):
    """Return active credentials in a tuple (url, user, token, auth_by)."""
    url, user, token, auth_by = default_credentials(url, token)
    if not token:
        access = security.Credentials(url)
        user, token = access.auth_pair()
        auth_by = access.source

    return (url, user, token, auth_by)


class APIWrapper(hvac.Client):
    """Wrapper for client API."""

    last_url = None

    def _get(self, url, **kwargs):
        """Remember last accessed URL."""
        self.last_url = urljoin(self._url, url)
        return hvac.Client._get(self, url, **kwargs)


class Connection(object):
    """Hashicorp Vault connection."""

    def __init__(self, url=None, token=None):
        self.url, self.user, self.token, self.auth_by = get_credentials(url, token)
        self.api = APIWrapper(url=self.url, token=self.token)

    def __str__(self):
        """Return human readable description of this connection."""
        return "Connection to {} [authenticated by {}'s token from {}]".format(
            self.url, self.user, self.auth_by or 'N/A')
