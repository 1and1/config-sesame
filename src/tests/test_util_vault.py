# *- coding: utf-8 -*-
# pylint: disable=wildcard-import, missing-docstring, no-self-use, bad-continuation
# pylint: disable=invalid-name, redefined-outer-name, too-few-public-methods
""" Test :py:mod:`config_sesame.util.vault`.
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

from config_sesame.util import vault


def test_Vault_token_is_read_from_token_file(mocker):
    mocker.patch('config_sesame.util.vault.VAULT_TOKEN_FILE', __file__)
    mocker.patch.dict('os.environ', VAULT_TOKEN='')

    url, user, token, auth_by = vault.default_credentials()

    assert token == '# *- coding: utf-8 -*-'
    assert auth_by == 'vault-token-file'
