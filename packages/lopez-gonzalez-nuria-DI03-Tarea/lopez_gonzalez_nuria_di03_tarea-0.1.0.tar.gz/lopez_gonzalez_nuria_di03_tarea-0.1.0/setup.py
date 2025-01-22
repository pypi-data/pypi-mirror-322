import sqlite3
import PySide6
from setuptools import setup, find_packages # type: ignore

setup(
    name='lopez_gonzalez_nuria_DI03_Tarea',
    version='0.1.0',
    packages=find_packages(include=['di_u3', 'di_u3.*']),
    install_requires=['PySide6'],  #sqlite3 no xq forma parte de la biblioteca de python
    test_suite='tests',
    include_package_data=True,
    description='Reserva de salones para eventos en hotel MiHotel',
    long_description=open('readme.txt').read(),
    long_description_content_type='text/plain',
    author='Nuria Lopez Gonzalez',
    author_email='nuria.lopezg1@gmail.com',
    url='', #sin especificar porque no la he subido a la web
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
