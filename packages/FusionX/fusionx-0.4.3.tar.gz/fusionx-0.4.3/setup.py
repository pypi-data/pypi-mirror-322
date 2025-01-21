from setuptools import setup, find_packages
setup(
    name="FusionX",
    version="0.4.3",
    packages=find_packages(),
    install_requires=["numpy", "scipy", "gdown"],
    author="Andy",
    author_email="mamaeva.anastas@gmail.com",
    description="A simple example private package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'print_A1=FusionX.cli:main',  
        ],
    },
    python_requires='>=3.9',
)
