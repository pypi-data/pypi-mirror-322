from setuptools import find_packages, setup

import aioagi

with open("README.rst", encoding="utf-8") as fh:
    README = fh.read()

tests_require = [
    "coverage",
    "pytest",
    "pytest-asyncio",
    "pytest-sugar",
    "pytest-cov",
]


setup(
    name="aioagi-ik",
    version=aioagi.VERSION,
    description="Async agi client/server framework (asyncio)",
    long_description=README,
    long_description_content_type="text/x-rst",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Communications :: Internet Phone",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    author="Shakurov Vadim Vladimirovich",
    author_email="apelsinsd@gmail.com",
    url="https://gitlab.com/VadimShakurov/aioagi.git",
    license="Apache License 2.0",
    keywords="aiogi asyncio asterisk telephony voip",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "aiohttp>=3.11,<4",
        "async_timeout>=4.0,<5",
    ],
    extras_require={
        "dev": [
            "ipdb",
            "ipython",
        ],
        "testing": tests_require,
    },
)
