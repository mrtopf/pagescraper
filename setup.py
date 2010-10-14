from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='webscraper',
      version=version,
      description="A html scraper for single web pages for extracting title, content and images",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='scraping html web',
      author='Christian Scholz',
      author_email='cs@comlounge.net',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          BeautifulSoup,
          lxml,
          simplejson,
          werkzeug,
          routes,
          pymongo
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
