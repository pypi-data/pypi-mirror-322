from setuptools import find_packages, setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pt2d",
    version="0.1.3",
    author="Aske T. Rove, Christian L. Bjerregaard, Mikkel W. Breinstrup",
    author_email="s224362@dtu.dk, s224389@dtu.dk, s224361@dtu.dk",
    description="Interactive path tracing in 2D medical images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://lab.compute.dtu.dk/QIM/tools/pt2d",
    packages=find_packages(include=["pt2d", "pt2d.*"]),
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'pt2d=pt2d:main'
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy<=1.26.4",
        "opencv_python>=4.9.0.80",
        "PyQt5>=5.15.11",
        "PyQt5_sip>=12.11.1",
        "scipy>=1.15.1",
        "scikit-image>=0.23.2"
    ]
)