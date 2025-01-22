from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Operating System :: Microsoft :: Windows",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3"
]
 
setup(
  name="gui_generator",
  version="2.0.0",
  description="The GUIgenerator module facilitates the creation of simple GUI applications.",
  long_description=open("README.rst").read(),
  long_description_content_type="text/x-rst",
  url="",  
  author="CPUcademy",
  author_email="cpucademy@gmail.com",
  license="MIT", 
  classifiers=classifiers,
  keywords="cpucademy CPUcademy GUIgenerator guigenerator tkinter GUI gui",
  packages=find_packages(),
  install_requires=[] 
)