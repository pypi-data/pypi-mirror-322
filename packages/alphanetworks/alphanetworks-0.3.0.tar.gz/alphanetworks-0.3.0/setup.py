from setuptools import setup, find_packages

setup(
    name="alphanetworks",
    version="0.3.0",
    description="Custom deep learning layers and hybrid models for image classification.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Team AlphaNetworks",
    author_email="ihteshamjahangir21@gmail.com.com",
    url="https://github.com/ihtesham-jahangir/alphanetworks",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.0",
        "numpy",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "alphanetworks=scripts.train_model:main"
        ]
    },
    python_requires=">=3.6",
)
