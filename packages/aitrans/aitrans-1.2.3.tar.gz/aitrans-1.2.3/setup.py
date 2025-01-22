from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aitrans",
    version="1.2.3",
    author="kilon",
    author_email="a15607467772@163.com",
    description="A powerful AI-powered translation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kilolonion/AITranslator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "aiohttp>=3.8.0",
        "httpx>=0.24.0",
        "tenacity>=8.0.0",
        "langdetect>=1.0.9"
    ],
    keywords="translation, ai, nlp, language, deep learning",
)
