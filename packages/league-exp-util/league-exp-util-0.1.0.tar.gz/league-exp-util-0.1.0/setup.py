from setuptools import setup, find_packages

setup(
    name="league-exp-util",  # Package name
    version="0.1.0",         # Initial version
    description="A utility to calculate League of Legends experience points.",
    long_description=open("README.md").read(),  # Use README for PyPI description
    long_description_content_type="text/markdown",
    author="JWasAway",
    author_email="JWasAway@Outlook.com",
    url="https://github.com/FieryAced/league-exp-util",  # GitHub or project link
    packages=find_packages(),  # Automatically finds modules in your package
    install_requires=[],       # List dependencies (empty if none)
    classifiers=[              # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",   # Minimum Python version
    keywords="league of legends xp calculator game utilities"
)