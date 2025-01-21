# This file is part of emzed (https://emzed.ethz.ch), a software toolbox for analysing
# LCMS data with Python.
#
# Copyright (C) 2020 ETH Zurich, SIS ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


import os

import numpy
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

install_requires = (
    "emzed>=3.0.0a22",
    "PyQt5",
    "PyQt5-Qt5",
    "guidata==1.7.7",
    "pythonqwt==0.5.5",
    "guiqwt303>=3.0.3",
    "matplotlib",
    "numpy",
)


ext_modules = cythonize(
    [
        Extension(
            "emzed_gui.optimized.optimized",
            [os.path.join("src", "emzed_gui", "optimized", "optimized.pyx")],
            include_dirs=[numpy.get_include()],
        )
    ]
)


setup(
    name="emzed_gui",
    version="3.0.0a24",
    description="",
    url="",
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    install_requires=install_requires,
    ext_modules=ext_modules,
    include_package_data=True,
)
