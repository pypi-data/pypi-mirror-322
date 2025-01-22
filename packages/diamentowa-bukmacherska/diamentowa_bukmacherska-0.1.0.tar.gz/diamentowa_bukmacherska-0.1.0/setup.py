from setuptools import setup, find_packages

setup(
    name="diamentowa_bukmacherska",
    version="0.1.0",
    description="Zaawansowana biblioteka do analiz bukmacherskich",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Twoje Imię",
    author_email="twoj.email@example.com",
    url="https://github.com/twoje-repozytorium/diamentowa_bukmacherska",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
