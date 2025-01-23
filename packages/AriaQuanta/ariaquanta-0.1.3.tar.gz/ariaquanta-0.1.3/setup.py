from setuptools import setup, find_packages

setup(
    name="AriaQuanta",  # Package name
    version="0.1.3",    # Initial version
    description="A quantum computing library",  # Short description
    long_description=open("README.md").read(),  # Readme as the long description
    long_description_content_type="text/markdown",
    author="mahmoudalipour",
    author_email="mahmoudalipour.d@gmail.com",
    url="https://github.com/MhmudAlpurd/ariaquanta.git",  # Update with your GitHub URL
    license="MIT",  # License type
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        "matplotlib==3.10.0" , "numpy==1.26.4", "scipy==1.15.1", "pandas==2.0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
)

