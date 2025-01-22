# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
{
    "name": "Letter Management + Operating Unit Integration",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_letter",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/outgoing_letter.xml",
        "security/res_group/incoming_letter.xml",
        "security/ir_rule/outgoing_letter.xml",
        "security/ir_rule/incoming_letter.xml",
        "views/outgoing_letter_views.xml",
        "views/incoming_letter_views.xml",
    ],
    "demo": [],
    "images": [],
}
