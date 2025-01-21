from setuptools import setup, find_packages

with open('LICENSE', 'r') as fh:
    license = fh.read()

description = 'Ultimate scraping engine powered by Chromium'

setup(
    name='scraper_engine_v2', # Package name
    version='0.1.0', # Package version
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    license=license,
    classifiers=[
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent"
    ],

    # Package definitions and requirements
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests-toolbelt'
    ],

    # Contact information
    author='Wimtop',
    url='https://github.com/Wimtop/scraper_engine_v2',

    # Tests
    test_suite='nose.collector',
    tests_require=['nose'],

    # Miscellaneous
    zip_safe=False,
)
