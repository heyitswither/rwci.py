from setuptools import setup
import re, os

requirements = ['websockets']

version = ''
with open('rwci/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
try:
    with open('README.md') as f:
        try:
            readme = f.read()
        except:
            readme = "RWCI API wrapper"
except:
    readme = "RWCI API Wrapper"


setup(name='rwci.py',
      author='heyitswither',
      author_email="joseph@josephbanks.me",
      url='https://github.com/heyitswither/rwci.py',
      version=version,
      packages=['rwci'],
      license='MIT',
      description='A python wrapper for RWCI API.',
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)
