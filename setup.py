from setuptools import setup, find_packages

setup(
    name='studi',
    version='1.0.5',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask>=0.12.0',
        'flask-restful>=0.3.0'
    ],
)
