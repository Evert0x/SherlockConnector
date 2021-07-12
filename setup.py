import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sherlock-connector",
    version="0.0.1",
    author="Sherlock Protocol",
    author_email="dev@sherlock.xyz",
    description="Connector for Sherlock V1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sherlock.xyz/",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "shercon = cli.shercon:cli",
        ],
    },
    install_requires=[
        "click==7.1.2",
        "requests==2.25.1",
        "pyyaml==5.4.1"
    ],
    python_requires='>=3.6',
)
