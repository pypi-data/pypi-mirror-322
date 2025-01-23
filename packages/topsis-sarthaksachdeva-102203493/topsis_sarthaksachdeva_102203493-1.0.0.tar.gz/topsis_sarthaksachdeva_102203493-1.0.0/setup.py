from setuptools import setup, find_packages

setup(
    name="topsis_sarthaksachdeva_102203493",
    version="1.0.0",
    author="Sarthak Sachdeva",
    author_email="your_email@example.com",
    description="A Python package for performing TOPSIS analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourgithubusername/Topsis-SarthakSachdeva-102203493",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
