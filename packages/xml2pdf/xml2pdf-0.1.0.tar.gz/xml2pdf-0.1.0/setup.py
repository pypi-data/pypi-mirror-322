from setuptools import setup, find_packages

setup(
    name="xml2pdf",
    version="0.1.0",
    author="Hirthickkesh",
    author_email="hirthickkeshpr@gmail.com",
    description="A Python library to convert XML files to PDF",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Higgy-debug/xml2pdf",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests>=2.25.0',
        'lxml>=4.9.0',
        'weasyprint>=59.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)