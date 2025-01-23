import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md to show on pypi
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.0'
DESCRIPTION = 'Utility_Function is a module designed to assist in Python programming. It defines several commonly used constants and functions, aimed at improving programming efficiency and code readability.'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    name="Utility_Function",
    version=VERSION,
    author="fengwenxi",
    author_email="yyxx1234567890q@dingtalk.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Utility', 'Function', 'Utility_Function', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)