from setuptools import find_packages, setup

setup(
    name="im8",
    version="1.2.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-package-name",
    packages=find_packages(),
    install_requires=["pyperclip==1.9.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# python setup.py sdist bdist_wheel
# twine upload --repository pypi dist/*