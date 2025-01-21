# setup.py
#

import setuptools

setuptools.setup(
  name='notebook-ai',
  version='0.1',
  author='Nikhil Kothari',
  description='Enables running AI functionality in Jupyter notebooks using IPython magics.',
  license='BSD',
  keywords='ai genai llm gemini vertexai jupyter interactive ipython',
  url='https://github.com/nikhilk/nbai',
  packages=[
    'nbai'
  ],
  install_requires = [
    'ipykernel'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Framework :: IPython',
    'Framework :: Jupyter',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: Apache Software License'
  ],
)
