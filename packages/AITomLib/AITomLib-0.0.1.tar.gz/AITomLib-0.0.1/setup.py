from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'AITomLib Python package'
LONG_DESCRIPTION = 'AITomLib Python package with a slightly longer description'
EMAIL = 'tomenglish23@gmail.com'

# Setting up
setup(
       # the name must match the folder name 'AITomLib'
        name="AITomLib", 
        version=VERSION,
        author="TE23",
        author_email=EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add  addl packages along with your package. Eg: 'caer'
        keywords=['python', 'AITomLib'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)
