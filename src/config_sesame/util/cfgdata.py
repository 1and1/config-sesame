# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
""" Helpers for handling configuration data).
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
import collections

import yaml
from click.exceptions import UsageError


def load_all(filename):
    """Generate objects contained in ``filename``."""
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        with io.open(filename, encoding='utf-8') as handle:
            for obj in yaml.load_all(handle):
                yield obj
    else:
        raise UsageError("Unsupported file type (extension) in '{}'!".format(filename))


def is_mapping(obj):
    """Check if ``obj`` offers the mapping interface."""
    return isinstance(obj, (dict, collections.Mapping, collections.MappingView))


def merge_objects(namespace, obj):
    """Update ``namespace`` with data in ``obj``."""
    for key, val in obj.items():
        if key in namespace and is_mapping(namespace[key]) and is_mapping(val):
            merge_objects(namespace[key], val)
        else:
            namespace[key] = val


def read_merged_files(cfgfiles):
    """Read a list of hierachical config files, and merge their keys."""
    result = {}
    for cfgfile in cfgfiles:
        for obj in load_all(cfgfile):
            merge_objects(result, obj)
    return result
