from setuptools import setup, find_packages

setup(
    name='StatyaUKRRF',
    version='0.1',  
    packages=find_packages(),
    description='Это простая библиотека, которая предоставляет список статей, наказываемых по законодательству Российской Федерации.',
    author='Puxxalwl',
    author_email='ruslan544mc@gmail.com',
    install_requires=[],
    classifiers=[ 
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)