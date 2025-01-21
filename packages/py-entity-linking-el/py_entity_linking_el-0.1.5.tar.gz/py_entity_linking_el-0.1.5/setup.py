from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='py-entity-linking-el',
    version='0.1.5',
    packages=find_packages(),
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy==1.26.4",
        "SPARQLWrapper==2.0.0",
        "sentence_transformers==3.1.1",
        "aiohttp==3.9.5",
        "openai==1.55.3",
        "httpx==0.27.2",
        "beautifulsoup4==4.12.2",
        "nest_asyncio==1.5.8"
    ],
    author='Nikolas Kapralos',  
    description='A lightweight library for entity linking in Greek.',
    license_files = "LICENSE.txt",
    python_requires='>=3.10',

)