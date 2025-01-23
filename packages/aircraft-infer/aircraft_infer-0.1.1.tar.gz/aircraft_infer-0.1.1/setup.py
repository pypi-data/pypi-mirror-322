from setuptools import setup, find_packages

x = 0

y = 1

z = 1

version = "{}.{}.{}".format(x, y, z)


setup(
    name='aircraft-infer',
    version=version,
    description='A python framework for distributed inference by arbitrary platform',
    url='',
    author='WD',
    author_email='',
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
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
