from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='syncgandidns',
    version='0.0.1',
    description='Sync a dynamic IP address with a Gandi DNS domain entry.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.6',
    url='https://github.com/RatJuggler/sync-gandi-dns',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'syncgandidns = syncgandidns.__main__:syncgandidns',
        ]
    },
    install_requires=[
        # Check latest releases on piwheels: https://www.piwheels.hostedpi.com/
        'click ==7.1.1',
        'requests ==2.23.0'
    ],
    test_suite='tests',
    tests_require=[
        'coverage',
        'flake8',
        'testfixtures',
        'tox'
    ],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: Name Service (DNS)'
    ]
)
