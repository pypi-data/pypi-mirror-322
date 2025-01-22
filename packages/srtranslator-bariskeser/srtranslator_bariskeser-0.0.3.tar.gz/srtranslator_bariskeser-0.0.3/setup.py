from pathlib import Path
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="srtranslator-bariskeser",
    description="Özel bir çevirmen kullanarak bir .SRT dosyasını çevirin",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/barkeser2002/srtranslator-bariskeser",
    version="0.0.3",
    author="bariskeser2002",
    author_email="info@bariskeser.com",
    license="FREE",
    python_requires=">=3.6",
    install_requires=requirements,
    packages=find_packages(),
    keywords=["python", "srt", "diller", "çevirmen", "altyazılar"],
)
