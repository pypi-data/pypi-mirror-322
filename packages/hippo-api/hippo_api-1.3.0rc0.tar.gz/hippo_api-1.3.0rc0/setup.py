from setuptools import setup, find_packages
import datetime

with open("requirements.txt") as f:
    required = f.read().splitlines()

build_pkgs = [
    i
    for i in find_packages(exclude=["*.tests", "*.tests.*", "tests"])
    if i.startswith("transwarp")
]

setup(
    name="hippo_api",
    version=f"1.3.0rc0",
    description="Transwarp Hippo API",
    author="transwarp",
    packages=build_pkgs,  # find_packages(exclude=["*.tests", "*.tests.*", "tests"]), # 识别带__init__.py的目录为包；排除tests等
    python_requires=">=3.8.0",
    install_requires=required,
)
