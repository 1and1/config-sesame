# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" 'login' command.
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

import sys

try:
    import keyring
except ImportError:
    keyring = None

from click.exceptions import UsageError
from rudiments import security
from rudiments.reamed import click

from .. import config
from ..util import vault


@config.cli.command()
@click.pass_context
def login(ctx):
    """Set or change Vault login credentials in your keyring."""
    if not keyring:
        raise UsageError("'keyring' support is not available, please read"
            " 'https://config-sesame.readthedocs.io/en/latest/deploy.html'!", ctx=ctx)
    url, user, token, _ = vault.default_credentials()
    if not url:
        raise UsageError("You MUST provide a VAULT_ADDR!", ctx=ctx)
    if token:
        click.secho("WARN: You have a VAULT_TOKEN variable in your environment,"
                    " which will override any keyring credentials!",
                    fg='yellow', bg='black', bold=True, reverse=True)

    click.echo("Please enter credentials for storing in {}.{}..."
               .format(keyring.get_keyring().__class__.__module__, keyring.get_keyring().__class__.__name__))
    access = security.Credentials(url)
    user, token = access.auth_pair(force_console=True)  # Prompt for new password
    keyring.set_password(url, user, token)
    click.echo("Updated {}'s password (token) for {}".format(user, url))
