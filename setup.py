import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="honeybee-grasshopper-core",
    use_scm_version = True,
    setup_requires=['setuptools_scm'],
    author="Ladybug Tools",
    author_email="info@ladybug.tools",
    description="Core Honeybee plugin for Grasshopper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ladybug-tools/honeybee-grasshopper-core",
    packages=setuptools.find_packages(exclude=["samples"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: IronPython",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
)
