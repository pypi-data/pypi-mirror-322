from setuptools import setup, find_packages

setup(
    name="funksignal",
    version="0.1.0",
    author="Dreamfarer",
    description="funksignal is a signaling library for event-driven programming",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dreamfarer/funksignal",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
