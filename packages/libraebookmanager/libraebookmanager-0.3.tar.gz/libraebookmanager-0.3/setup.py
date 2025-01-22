from setuptools import setup, find_packages

setup(
    name="libraebookmanager",
    author="Araz Shah",
    author_email="araz.shah@gmail.com",
    description="libra is a Python package designed to help you organize and explore your eBook collection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/arazshah/libra",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "python-magic",
        "PyPDF2",
        "ebooklib",
        'pymupdf'
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "libraebookmanager=libraebookmanager.main:main",
        ],
    },
)
