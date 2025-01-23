from setuptools import setup, find_packages


package = "judobase"
requirements = [
    "aioresponses>=0.7.7",
    "aiohttp>=3.11.11",
    "pydantic>=2.10.5",
    "setuptools>=75.6.0"
]
test_requirements = [
    "pytest>=8.3.4",
]


setup(
    name=package,
    version="0.1.0",
    author="ddzgoev",
    author_email="ddzgoev@gmail.com",
    description="Python Judobase API async client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DavidDzgoev/judobase",
    packages=[
        'judobase',
    ],
    package_dir={'judobase': 'judobase'},
    license="MIT",
    zip_safe=False,
    keywords='judobase,wrapper,client,async,api',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    tests_require=test_requirements,
)
