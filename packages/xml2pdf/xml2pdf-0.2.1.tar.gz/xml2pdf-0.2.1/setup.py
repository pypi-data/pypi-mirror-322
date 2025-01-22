from setuptools import setup, find_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xml2pdf",
    version="0.2.1",  # Increment version number
    author="Hirthickkesh",
    author_email="hirthickkeshpr@gmail.com",
    description="A tool to convert XML files to PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Higgy-debug/xml2pdf",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'lxml',
        'weasyprint',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)