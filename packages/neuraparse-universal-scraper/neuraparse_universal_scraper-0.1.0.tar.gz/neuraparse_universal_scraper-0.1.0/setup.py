from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='neuraparse-universal-scraper',
    version='0.1.0',
    author='Adınız',
    author_email='email@example.com',
    description='Universal web scraper package under neuraparse namespace',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kullaniciadi/neuraparse-universal-scraper',
    packages=find_packages(),
    namespace_packages=['neuraparse'],
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'requests',
        'lxml',
        'html5lib',
        'undetected-chromedriver',
    ],
    entry_points={
        'console_scripts': [
            'neuraparse-universal-scrape=neuraparse.universal_scraper.scraper:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
