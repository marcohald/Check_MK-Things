#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# Example Output:
#
#

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    Service,
)


def parse_prism_vm_tools(string_table):
    import ast
    parsed = {}
    parsed = ast.literal_eval(string_table[0][0])
    return parsed


register.agent_section(
    name="prism_vm_tools",
    parse_function=parse_prism_vm_tools,
)


def discovery_prism_vm_tools(section) -> DiscoveryResult:
    yield Service()


def check_prism_vm_tools(params, section) -> CheckResult:
    state = 0
    message = ""
    tool_install = section["installedVersion"]
    tool_enabled = section["enabled"]

    if tool_install == None:
        message += "No Tools installed"
    else:
        message += "Tools with version %s installed" % tool_install
        if tool_enabled == False:
            state = 1
            message += " but not enabled"

    yield Result(state=State(state), summary=message)


register.check_plugin(
    name="prism_vm_tools",
    service_name="NTNX VMTools",
    sections=["prism_vm_tools"],
    check_default_parameters={
        'tool_state': 0,
    },
    discovery_function=discovery_prism_vm_tools,
    check_function=check_prism_vm_tools,
    check_ruleset_name="prism_vm_tools",
)
