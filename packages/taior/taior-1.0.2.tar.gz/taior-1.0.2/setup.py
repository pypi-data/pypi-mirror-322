from setuptools import setup, find_packages

setup(
    name='taior',
    version='1.0.2',
    author='Taior Project',
    author_email='livrasand@outlook.com',
    description='The Amnesic Incognito Oblivious Routing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/taiorproject/taior',  
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.6',  
    install_requires=[
        'cryptography',  
        'pycryptodome', 
    ],
    entry_points={
        'console_scripts': [
            'taior=taior.main:main', 
        ],
    },
)