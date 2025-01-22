from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="ndevsecuritychecker",
    version="0.1.1",
    description="A project module for my coding class, that will serve me after.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Ilian",
    keywords=["dev", "utils", "Checker", "Security"],
    url="https://gitlab.com/bts-ciel-a1/base-project-structure/-/tree/ige/dev_utils?ref_type=heads",
    download_url="https://pypi.org/"
)

install_requires = [
    "colorama<=0.4.6",
    "pytest<=8.3.4",
    "pytest-cov<=6.0.0",
    "rich<=13.9.4"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)