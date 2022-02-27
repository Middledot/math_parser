import setuptools

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

packages = ["math_parser.py"]

setuptools.setup(
    name="disno",
    version="0.1.1",
    author="Middledot",
    author_email="middledot.productions@gmail.com",
    description="A math expression resolver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Middledot/MathParser",
    project_urls={
        "Issue Tracker": "https://github.com/Middledot/MathParser/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=packages,
    python_requires=">=3.7",
)
