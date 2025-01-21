from setuptools import setup, find_packages
import requests, flask, django

setup(
    name='ykx-lab',
    version='0.2.0',
    author='RockyYin',
    author_email='yinkaixuan0213@gmail.com',
    description='personal tools for everyone.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/littlegump/ykx-lab',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "flask",
        "django",
    ],
    include_package_data=True,
)
