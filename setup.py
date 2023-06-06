from setuptools import find_packages, setup

long_description = open("README.md").read()

setup(
    name="ScenarioReducer",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/DanieleGioia/ScenarioReducer",
    license="LICENSE.txt",
    author="Daniele Giovani Gioia, pdb5627",
    author_email="daniele.gioia@polito.it",
    description="Scenario Reduction Algorithms in Stochastic Programming",
    long_description=long_description,
    setup_requires=["numpy"],
    keywords='stochastic programming, probability metric, scenario reduction, scenario tree',
    install_requires=["scipy", "statsmodels", "numba", "pytest"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
