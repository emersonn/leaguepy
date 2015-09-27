from setuptools import setup, find_packages

setup(
    name='leaguepy',
    version='0.1',
    description='leaguepy',
    classifiers=[],
    keywords='',
    author='Emerson Matson',
    author_email='emersonn@uw.edu',
    url='',
    packages=['league'],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'bamboo-cli = bamboo.cli:main'
        ]
    },
    extras_require={
        'test': [
            'mock',
        ]
    }
)
