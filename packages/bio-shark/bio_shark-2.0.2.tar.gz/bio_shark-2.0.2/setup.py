import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = ""
    for line in fh:
        if line.startswith("## Developer section"):
            break
        long_description += line


with open(os.path.join(here, 'src/VERSION')) as fv:
    version = fv.read().strip()

setup(
    name="bio-shark",
    version=version,
    description="SHARK (Similarity/Homology Assessment by Relating K-mers)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Willis Chow <chow@mpi-cbg.de>, Soumyadeep Ghosh <soumyadeep11194@gmail.com>, "
           "Anna Hadarovich <hadarovi@mpi-cbg.de>, Agnes Toth-Petroczy <tothpet@mpi-cbg.de>, Maxim Scheremetjew <schereme@mpi-cbg.de>",
    author_email="chow@mpi-cbg.de",
    url="https://git.mpi-cbg.de/tothpetroczylab/shark",
    project_urls={
        "Homepage": "https://git.mpi-cbg.de/tothpetroczylab/shark",
        "Documentation": "https://git.mpi-cbg.de/tothpetroczylab/shark/-/blob/master/README.md",
        "Funding": "https://www.mpi-cbg.de/",
        "Repository": "https://git.mpi-cbg.de/tothpetroczylab/shark",
        "Issue tracker": "https://git.mpi-cbg.de/tothpetroczylab/shark/-/issues",
    },
    keywords=["intrinsically disordered protein regions", "motif detection", "IDRs", "sequence-to-function", "alignment-free", "machine learning", "homology detection"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    package_dir={"bio_shark": "src"},
    package_data={"bio_shark": ["VERSION", "data/*"]},
    python_requires=">=3.8,<3.13",
    install_requires=[
        "requests ~=2.32.0",
        "catboost >=1.0.0",
        "matplotlib >=3.5",
        "pandas >=1.3",
        "logomaker ~=0.8",
        "alfpy ~=1.0.6",
        "numpy <2.0.0",
        "seaborn==0.13.2",
    ],
    entry_points={
        "console_scripts": [
            "shark-score = bio_shark.dive.calculate_kmer_scores:main",
            "shark-dive = bio_shark.dive.prediction:main",
            "shark-capture = bio_shark.capture.compute:main",
        ]
    },
)
