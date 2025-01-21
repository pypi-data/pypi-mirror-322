"""Setup module.
"""

import setuptools

setuptools.setup(
  name='notebook-ai',
  version='0.1.1',
  author='Nikhil Kothari',
  description='Enables Jupyter magics to define and run AI/LLM prompts.',
  license='Apache',
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
    'Framework :: Jupyter :: JupyterLab :: Extensions',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Software Development :: Libraries'
  ],
)
