from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='visualdsa',
  version='0.0.4',
  description='Generates visually appealing representations of data structures.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Sutheera Pitakpalin',
  author_email='s.pitakpalin@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data structure', 
  packages=find_packages(),
  install_requires=['matplotlib']
)