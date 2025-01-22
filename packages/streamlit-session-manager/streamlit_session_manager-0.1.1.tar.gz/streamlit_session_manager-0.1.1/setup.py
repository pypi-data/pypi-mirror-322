from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="streamlit-session-manager",
    version="0.1.1",
    author="5X",
    author_email="support@5x.co",
    license="MIT",
    description="A session manager for Streamlit applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/5X-nextgen-customer-repo-prod/streamlit_session_manager.gitc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "extra-streamlit-components"
    ],
)