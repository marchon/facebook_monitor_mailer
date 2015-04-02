import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'pyramid_mailer==0.14',
    'requests==2.6',
    'repoze.sendmail==4.1',
    ]

setup(
    name='ielts',
    version='0.0',
    description='ielts',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons pyramid_mailer facebook',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="ielts",
    )
