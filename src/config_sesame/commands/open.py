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

import io
import sys

from pyaml import dump as ppyaml
from click.exceptions import UsageError
from rudiments.reamed import click

from .. import config
from ..util import cfgdata, vault

SECRETS_POSTFIX = '_secret'


def vault_key(reference):
    """Validate a vault key reference."""
    if not reference.startswith('vault:'):
        raise UsageError('Expected a "vault:..." reference, got "{}" instead'.format(reference))
    return reference.split(':', 1)[1].strip('/')


def lookup_key(key, bases, conn):
    """Look for a key in the given bases."""
    for base in bases:
        key_path = ''.join((base, '/', key)).strip('/')
        secret = conn.api.read(key_path)
        ##print(repr((key_path, secret)))
        if secret is not None:
            result = secret['data']
            if len(result) == 1:
                result = result.get('value', result)
            return result, conn.api.last_url

    raise UsageError('Cannot find key "{}" in any of these bases: {}.'
                     .format(key, ', '.join(x or '/' for x in bases)))


def lookup_secrets(obj, bases, conn):
    """Scan ``obj`` for secrets, and look them up."""
    bases = [x.strip('/') for x in bases or ['']]

    result = {}
    if cfgdata.is_mapping(obj):
        for key, val in obj.items():
            if key.endswith(SECRETS_POSTFIX):
                base_key = key[:-len(SECRETS_POSTFIX)]
                result[base_key], result[key + '_url'] = lookup_key(vault_key(val), bases, conn)
            else:
                subtree = lookup_secrets(val, bases, conn)
                if subtree:
                    result[key] = subtree
    return result


@config.cli.command(name='open')
@click.option('-b', '--base', 'bases', metavar='PATH [-b ...]', multiple=True,
              help='Look up keys relative to the given base path(s).')
@click.option('-o', '--output', 'outfile', metavar='FILE',
              type=click.Path(), show_default=True, default='secrets.yml',
              help='Write output to given file,'
                   ' use "-o-" for printing clear text secrets to stdout.')
@click.argument('cfgfile', metavar='CFGFILE [...]', nargs=-1)
@click.pass_context
def open_command(ctx, cfgfile=None, bases=None, outfile=''):
    """Open vault and amend configuration file(s)."""
    if not cfgfile:
        raise UsageError("You provided no configuration file names!", ctx=ctx)

    try:
        conn = vault.Connection()
    except ValueError as cause:
        if "target" in str(cause):
            click.serror("{} -- forgot to edit configuration or set VAULT_ADDR?", cause)
        else:
            raise

    data = cfgdata.read_merged_files(cfgfile)
    secrets = lookup_secrets(data, bases, conn)
    #ppyaml(cfgdata, sys.stdout)
    if outfile in ('', '-'):
        ppyaml(secrets, sys.stdout)
    else:
        if not ctx.obj.quiet:
            click.echo('Writing secrets to "{}"...'.format(outfile))
        with io.open(outfile, 'w', encoding='utf-8') as handle:
            ppyaml(secrets, handle)
