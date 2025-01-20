from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='parametric-ttl-cache',
    version='1.0',
    author='Yongho Hwang',
    author_email='jogakdal@gmail.com',
    description='A function-level memory cache that supports Time To Live (TTL)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jogakdal/python_ttl_cache',
    install_requires=['collections', 'inspect', 'expiringdict'],
    packages=find_packages(exclude=[]),
    keywords=['cache', 'memory cache', 'ttl cache', 'function cache', 'cache decorator', 'parametric cache', 'jogakdal'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
