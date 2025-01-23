# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atomic_physics',
 'atomic_physics.atoms',
 'atomic_physics.examples',
 'atomic_physics.ions',
 'atomic_physics.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.0,<2.0.0', 'scipy>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'atomic-physics',
    'version': '2.0.1',
    'description': 'Lightweight python library for calculations based on atomic structure',
    'long_description': 'None',
    'author': 'hartytp',
    'author_email': 'thomas.peter.harty@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
