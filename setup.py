#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from glob import glob

import mkdatafiles
data_files = mkdatafiles.get_data_files()
data_files.append(("/usr/share/applications/", ["Peru_Learns_English.desktop"]))
data_files.append(("/usr/share/applications/",
                   ["Peru_Learns_English_TV.desktop"]))

setup(
    name="Peru_Learns_English",
    version="1.1",
    author="SomosAzucar",
    author_email="laura@somosazucar.org",
    url="http://pe.sugarlabs.org/ir/Peru%20Learns%20English",
    license="GPL3",

    scripts=["peru_learns_english",
             "peru_learns_english_uninstall", "peru_learns_english_tv"],

    data_files=data_files

)
