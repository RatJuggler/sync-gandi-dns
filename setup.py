from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='syncgandidns',
    version='0.0.3',
    description='Sync a dynamic IP address with a Gandi DNS domain entry.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='gandi dns',
    author='John Chase',
    author_email='ratteal@gmail.com',
    python_requires='>=3.7',
    url='https://github.com/RatJuggler/sync-gandi-dns',
    project_urls={
        "Documentation": "https://github.com/RatJuggler/sync-gandi-dns",
        "Code": "https://github.com/RatJuggler/sync-gandi-dns",
        "Issue tracker": "https://github.com/RatJuggler/sync-gandi-dns/issues",
    },
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'syncgandidns = syncgandidns.__main__:syncgandidns',
        ]
    },
    install_requires=[
        # Check latest releases on piwheels: https://www.piwheels.org/
        'click ==7.1.2',
        'requests ==2.25.1'
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
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: Name Service (DNS)'
    ]
)
