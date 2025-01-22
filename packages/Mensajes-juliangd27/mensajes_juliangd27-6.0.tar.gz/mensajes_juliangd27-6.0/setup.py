from struct import pack
from setuptools import setup, find_packages 

setup(
    name = 'Mensajes-juliangd27',
    version = '6.0',
    description = 'Un paquete para saludar y despedir',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author = 'Julián Gómez Durso',
    author_email ='juliangd27@gmail.com',
    url = 'https://www.julian.dev',
    license_files = ['LICENSE'],
    packages = find_packages(),
    scripts = [],
    
    install_requires = [paquete.strip() for paquete in open("requirements.txt").readlines()],
    classifiers= ['Environment :: Console',
                  'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities'
                  ]
)
