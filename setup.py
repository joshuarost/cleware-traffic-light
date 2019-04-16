from setuptools import setup, find_packages

setup(
    name='cleware-traffic-light',
    version='1.0.0',
    description='Python3 modul and cli tool to controll the Cleware traffic light',
    author='Josh Rost',
    author_email='joshua.s.rost@gmail.com',
    packages=find_packages(),
    install_requires=['pyusb'],
    entry_points={
        'console_scripts': ['ctl=traffic_light'],
    }
)
