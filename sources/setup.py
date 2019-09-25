from setuptools import setup

setup(
    name='blockswarm',
    version='0.1.0',
    packages=['robot_swarm', 'bs_blockchain'],
    package_dir={'': 'sources'},
    url='https://misti.etsisi.upm.es',
    license='GPLv3',
    author='Iván García-Alcaide',
    author_email='igarcia@etsisi.upm.es',
    description='Blockchain for swarm robotics implementation'
)
