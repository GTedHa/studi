from setuptools import setup, find_packages

setup(
    name='studi',
    version='1.0.19',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask>=0.12.0',
        'flask-restful>=0.3.0',
        'gunicorn>=19.7',
        'beautifulsoup4>=4.4.0'
    ],
)
