# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ak']

package_data = \
{'': ['*']}

install_requires = \
['colored>=2.2.4,<3.0.0', 'terminaltables>=3.1.10,<4.0.0']

entry_points = \
{'console_scripts': ['basic = examples.basic:main']}

setup_kwargs = {
    'name': 'akconfig',
    'version': '0.1.4',
    'description': 'A configuration management for global variables in python projects.',
    'long_description': '# akconfig\n\nA configuration management for global variables in python projects.\nakconfig is a small python class that takes global variables and lets you manipulate them quickly. the advantage can be that you still need manipulations that are to be changed via arguments, or via environment variables. when executing the example file basic.py, it quickly becomes obvious what this is intended for.\n\n\n## example\n\n`$ poetry run basic`\n\n## get help\n\n```\npoetry run basic --help\nUsage: basic [OPTIONS]\n\nOptions:\n  -c, --config <TEXT TEXT>...  Config parameters are: VAR_A, VAR_B, VAR_C,\n                               VAR_D, VAR_E, VAR_F, VAR_G, VAR_H, VARS_MASK\n  -f, --force-env-vars         Set argument if you want force environment\n                               variables\n  --help                       Show this message and exit.\n```',
    'author': 'dapk',
    'author_email': 'dapk@gmx.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
