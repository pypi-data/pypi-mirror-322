import setuptools
from pathlib import Path

setuptools.setup(
    name="tina_env",
    version="0.0.1",
    description="A openAI Gym env for tina",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["tina_env.*"]),
    install_requires=["gym"]
)