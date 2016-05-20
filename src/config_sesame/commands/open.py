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
import os
import sys

import yaml
from pyaml import dump as ppyaml
from click.exceptions import UsageError
from rudiments.reamed import click

from .. import config


def load_all(filename):
    """Generate objects contained in ``filename``."""
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        with io.open(filename, encoding='utf-8') as handle:
            for obj in yaml.load_all(handle):
                yield obj
    else:
        raise UsageError("Unsupported file type (extension) in '{}'!".format(filename))


def read_merged_files(cfgfiles):
    """Read a list of hierachical config files, and merge their keys."""
    result = {}
    for cfgfile in cfgfiles:
        for obj in load_all(cfgfile):
            result.update(obj) # TODO: sensible merging strategy
    return result


@config.cli.command(name='open')
@click.argument('cfgfile', nargs=-1)
@click.pass_context
def open_command(ctx, cfgfile=None):
    """Open vault and amend configuration file(s)."""
    if not cfgfile:
        raise UsageError("You provided no configuration file names!", ctx=ctx)

    cfgdata = read_merged_files(cfgfile)
    ppyaml(cfgdata, sys.stdout)
