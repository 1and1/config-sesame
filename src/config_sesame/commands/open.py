# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation, too-few-public-methods
""" 'open' command.
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

from pyaml import dump as ppyaml
from click.exceptions import UsageError
from rudiments.reamed import click

from .. import config
from ..util import cfgdata

SECRETS_POSTFIX = '_secret'


def lookup_secrets(obj):
    """Scan ``obj`` for secrets, and look them up."""
    result = {}
    if cfgdata.is_mapping(obj):
        for key, val in obj.items():
            if key.endswith(SECRETS_POSTFIX):
                result[key[:-len(SECRETS_POSTFIX)]] = "THIS WOULD BE LOOKED UP"
            else:
                subtree = lookup_secrets(val)
                if subtree:
                    result[key] = subtree
    return result


@config.cli.command(name='open')
@click.argument('cfgfile', nargs=-1)
@click.pass_context
def open_command(ctx, cfgfile=None):
    """Open vault and amend configuration file(s)."""
    if not cfgfile:
        raise UsageError("You provided no configuration file names!", ctx=ctx)

    data = cfgdata.read_merged_files(cfgfile)
    secrets = lookup_secrets(data)
    #ppyaml(cfgdata, sys.stdout)
    ppyaml(secrets, sys.stdout)
