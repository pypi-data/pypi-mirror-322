import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='dtarot',  
     version='2.1',
     scripts=['dtarot'] ,
     author="Lord Imbrius the Despondent",
     author_email="darthferrett@gmail.com",
     description="Discordian Tarot reading generator",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/lorimbrius/dtarot",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
	 "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
         "Operating System :: OS Independent",
     ],
 )
