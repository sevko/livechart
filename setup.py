"""
Set up the `livechart` tool.
"""

import setuptools

with open("README.rst") as file_:
	long_description = file_.read()

setuptools.setup(
	name="livechart",
	description="A CLI utility for charting data on the fly.",
	long_description=long_description,
	version="0.0.2",
	url="https://github.com/sevko/livechart",
	author="Severyn Kozak",
	author_email="severyn.kozak@gmail.com",
	entry_points={"console_scripts": ["livechart=livechart.script:run"]},
	packages=setuptools.find_packages(),
	install_requires=["matplotlib == 1.4.3"],
	license="MIT"
)
