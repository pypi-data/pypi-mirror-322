from setuptools import setup, find_packages

setup(
    name='topsis-Pranav-102203059',  
    version='1.1',
    description='A Python package to implement the TOPSIS method',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Pranav Jain',
    author_email='pjain_be22@thapar.edu',
    packages=find_packages(),
    install_requires=[ 
        'pandas',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
