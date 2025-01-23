"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import re
import sys
from os import path

import click
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent

import hcs_cli.service as hcs


@click.group
def operator():
    """Commands for intelligent operator."""
    pass


@operator.command
@cli.org_id
@click.argument("name", required=True)
@cli.wait
def run(org: str, name: str, wait: str, **kwargs):
    """Run a specific operator for a specific org."""
    org_id = cli.get_org_id(org)
    task = hcs.scm.operator.run(org_id=org_id, name=name)
    if wait == "0":
        return task

    return hcs.task.wait(org_id=org_id, namespace="scm", task=task, timeout=wait)


@operator.command
@cli.org_id
@click.argument("name", required=True)
def logs(org: str, name: str, **kwargs):
    """Get logs of an operator."""
    org_id = cli.get_org_id(org)
    return hcs.scm.operator.logs(org_id=org_id, name=name)
