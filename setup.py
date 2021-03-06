from setuptools import setup, find_packages
import os


version = '1.0'


tests_require = [
    'plone.app.testing',
    'ftw.builder',
    'pyquery',
    'ftw.testbrowser',
    ]


setup(name='ftw.activitystation',
      version=version,
      description="Provides an action for plone.app.contentules that allows "
                  "posting activities to activity station.",
      long_description=(open('README.rst').read() + '\n' +
                        open(os.path.join('docs', 'HISTORY.txt')).read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='',
      author='4teamwork',
      author_email='info@4teamwork.ch',
      url='http://www.4teamwork.ch',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'ftw.upgrade>=1.7',
          'Plone',
          'plone.api',
          'plone.app.contentrules',
          'plone.contentrules',
          'requests',
          'setuptools',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
