import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="gptsummarizer",
    version="0.0.5",
    author="Dev Halder",
    author_email="dev.devojoyti@gmail.com",
    description="A lightweight library to summarize long texts using GPT models",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/devojoyti/gpt-summarizer-python",
    packages=setuptools.find_packages(),
    install_requires=["tiktoken", "openai"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
