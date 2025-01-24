from setuptools import setup, find_packages

setup(
    name="JsonXL",
    version="1.0.0",
    description="A utility to convert JSON files to Excel sheets",
    author="Mahesh",
    author_email="maheshyamana123@gmail.com",
    packages=find_packages(),  # Automatically include `jsontoxl`
    install_requires=[
        "openpyxl",  # Only openpyxl is required
    ],
    entry_points={
        "console_scripts": [
            "jsontoxl=jsontoxl.converter:json_to_excel",  # Command-line access
        ],
    },
)

