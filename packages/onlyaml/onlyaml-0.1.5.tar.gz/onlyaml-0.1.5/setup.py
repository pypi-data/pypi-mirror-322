from setuptools import setup, find_packages

x = 0

y = 1

z = 5

version = "{}.{}.{}".format(x, y, z)


setup(
    name='onlyaml',
    version=version,
    description='A python lib impose your program only accept yaml file as CL argument',
    url='https://github.com/shuds13/pyexample',
    author='WD',
    author_email='',
    license='MIT',
    packages=find_packages(),
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
