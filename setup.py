from setuptools import setup, find_packages


requires = []


setup(name='ramses_example',
      version='0.0.1',
      description='ramses_example',
      long_description='',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="ramses_example",
      entry_points="""\
      [paste.app_factory]
          main = ramses_example:main
      """)
