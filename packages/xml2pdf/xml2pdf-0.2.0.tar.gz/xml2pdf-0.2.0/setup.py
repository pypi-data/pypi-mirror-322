from setuptools import setup, find_packages

setup(
    name="xml2pdf",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'requests',
        'lxml',
        'weasyprint',
    ],
    python_requires=">=3.6",
)