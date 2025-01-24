VERSION = "0.0.1"

from setuptools import setup, find_packages

setup(
    name='opengrep',
    version=VERSION,   
    description='',
    long_description="opengrep",
    long_description_content_type="text/markdown",
    url='',
    author='Zerooo',
    author_email='',
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'tests.*', 'release']),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'opengrep=opengrep.main:main',
        ],
    },
    license='MIT',
    install_requires=[
        'boto3',
        'PyYAML',
        'jmespath',
        'rich',
        'setuptools',
        'patool',
        'pydrive2',
        'appdirs',
        'tqdm',
        'funcy',
        'fsspec',
    ],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    classifiers=[
        'Intended Audience :: Developers',
    ],
    keywords='opengrep grep',
)
