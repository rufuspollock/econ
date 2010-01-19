from setuptools import setup, find_packages

setup(
    name='ukgov_finances_cra',
    version='0.1',
    # Name of License for your project
    # Suitable open licenses can be found at http://www.opendefinition.org/licenses/
    license='PDDL',

    # Title or one-line description of the package
    description='Country and Regional Analyses (CRA) - UK Government Finances',

    # URL of project/package homepage
    url='http://www.hm-treasury.gov.uk/pesp_cra.htm',

    # Download url for this package if it has a specific location
    download_url='http://www.hm-treasury.gov.uk/d/cra_2009_db.xls',

    # Space-separated keywords/tags
    keywords='ukgov, country-uk, gov, size-medium, format-csv, format-xls',

    # Notes or multi-line description for your project (in markdown)
    long_description='''

    ''',

    author='UK Government (HMT)',

    maintainer='Rufus Pollock',

    # Ignore from here onwards
    package_dir={'ukgov_finances_cra': ''},
    packages=find_packages(),
    include_package_data=True,
    # do not zip up the package into an 'Egg'
    zip_safe=False,
)
