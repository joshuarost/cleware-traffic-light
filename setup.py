from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as desc_file:
    long_description = desc_file.read()

setup(
    name='cleware-traffic-light',
    version='1.0.6',
    description='Python3 modul and cli tool to controll the Cleware traffic light',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Josh Rost',
    author_email='joshua.s.rost@gmail.com',
    url='https://github.com/joshrost/cleware-traffic-light',
    packages=find_packages(),
    install_requires=['pyusb'],
    entry_points={
        'console_scripts': ['ctl=traffic_light.__main__:main'],
    }
)
