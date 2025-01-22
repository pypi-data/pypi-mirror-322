# setup.py

from setuptools import find_packages, setup

from maitai_common.version import version

setup(
    name="maitai-python",
    version=version,
    packages=find_packages(
        exclude=("maitai_back", "maitai_back.*"),
        include=(
            "maitai.*",
            "maitai",
            "maitai_common",
            "maitai_common.*",
            "maitai_models",
            "maitai_models.*",
        ),
    ),
    install_requires=[
        "requests",
        "openai>=1.34.0",
        "httpx",
        "aiohttp",
        "websocket-client",
    ],
    # Optional metadata
    author="Maitai",
    author_email="support@trymaitai.ai",
    description="Maitai SDK for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://docs.trymaitai.ai",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
