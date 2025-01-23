from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-clipboard",
    version="0.0.6",
    author="Wenfeng Sui",
    author_email="suiwenfeng@qq.com",
    description="Streamlit component that support copy and paste clipboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitcode.com/acl/streamlit-clipboard.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.41.1",
    ],
    extras_require={
        "devel": [
        ]
    }
)
