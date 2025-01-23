from setuptools import setup, find_packages

setup(
    name="excel_to_xml",
    version="1.0.0",
    author="Yagna",
    author_email="yagna781@gmail.com",
    description="A utility to convert Excel files to XML format",
    packages=find_packages(),
    install_requires=[
        "openpyxl",  # Include dependencies here
    ],
    entry_points={
        "console_scripts": [
            "excel_to_xml=excel_to_xml.converter:main",  # Replace `main` with your entry function
        ],
    },
)
