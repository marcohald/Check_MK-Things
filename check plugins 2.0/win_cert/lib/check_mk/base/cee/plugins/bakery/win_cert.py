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

from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register


def get_win_cert_files(conf: Dict[str, Any]) -> FileGenerator:
    yield Plugin(base_os=OS.WINDOWS, source=Path("win_cert.ps1"))

    validUntil = conf.get("valid", 30)
    certAuth = conf.get("auth", ".*")
    cfg_lines = ["$expireInDays = %s" % validUntil, "$issuerstring = '%s'" % certAuth]

    yield PluginConfig(
        base_os=OS.WINDOWS,
        lines=cfg_lines,
        target=Path("win_cert_cfg.ps1"),
    )


register.bakery_plugin(
    name="win_cert",
    files_function=get_win_cert_files,
)
