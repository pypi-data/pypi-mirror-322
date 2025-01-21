"""
Firmitas
Copyright (C) 2023-2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source code or
documentation are not subject to the GNU General Public License and may only
be used or replicated with the express permission of Red Hat, Inc.
"""


from pathlib import Path

import yaml
from cryptography import x509
from cryptography.hazmat.backends import default_backend

from firmitas.base.maintool import readcert
from firmitas.conf import logrdata, standard


class Difference:
    def __init__(self):
        # Populate a list of certificate files from the device
        certloca = Path(standard.certloca)
        self.certlist_from_device = [
            item.name
            for item in certloca.iterdir()
            if item.is_file() and ".crt" == item.suffix
        ]

        # Populate a list of certificate files from the config
        self.certdict = yaml.safe_load(Path(standard.hostloca).read_text())
        self.certlist_from_config = [item["path"] for item in self.certdict.values()]

        # Compute a list of certificate files to insert into the config
        self.to_insert = [
            item for item in self.certlist_from_device if item not in self.certlist_from_config
        ]

        # Compute a list of certificate files to remove from the config
        self.to_remove = [
            item for item in self.certlist_from_config if item not in self.certlist_from_device
        ]

    def insert(self):
        logrdata.logrobjc.warning(
            f"Inserting {len(self.to_insert)} certificate(s) that are now tracked"
        )

        for item in self.to_insert:
            certname = item.replace(".crt", "")
            certpath = Path(standard.certloca, item)
            try:
                certobjc = x509.load_pem_x509_certificate(certpath.read_bytes(), default_backend())
                readdata = readcert(certobjc)
            except ValueError:
                logrdata.logrobjc.error(
                    f"[{certname}] The specified X.509-standard TLS certificate could not be read"
                )
            else:
                logrdata.logrobjc.info(
                    f"[{certname}] The specified X.509-standard TLS certificate was read successfully"  # noqa : E501
                )
                self.certdict[certname] = {
                    "path": item,
                    "user": standard.username,
                    "certstat": {
                        "strtdate": readdata[0],
                        "stopdate": readdata[1],
                        "cstarted": readdata[2],
                        "cstopped": readdata[3],
                        "daystobt": readdata[4],
                        "daystodd": readdata[5],
                        "issuauth": readdata[6],
                        "serialno": readdata[7],
                    },
                    "notistat": {
                        "done": False,
                        "link": "",
                        "time": "",
                    }
                }

    def remove(self):
        logrdata.logrobjc.warning(
            f"Removing {len(self.to_remove)} certificate(s) that are not tracked"
        )

        for item in self.to_remove:
            certname = item.replace(".crt", "")
            self.certdict.pop(certname)
            logrdata.logrobjc.info(
                f"[{certname}] The specified X.509-standard TLS certificate was removed"
            )

    def action(self):
        # Do not act if the list is empty
        if len(self.to_insert) > 0:
            self.insert()

        # Do not act if the list is empty
        if len(self.to_remove) > 0:
            self.remove()

        with open(standard.hostloca, "w") as yamlfile:
            yaml.safe_dump(self.certdict, yamlfile)
