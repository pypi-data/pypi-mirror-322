from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='AskioCircleLib',
  version='0.0.1',
  description='circle class',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Askio',
  author_email='legoask@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='circle', 
  packages=find_packages(),
  install_requires=['pygame', 'math'] 
)