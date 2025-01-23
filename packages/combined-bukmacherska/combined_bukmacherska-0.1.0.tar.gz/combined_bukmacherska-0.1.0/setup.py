from setuptools import setup, find_packages

setup(
    name="combined_bukmacherska",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "pandas",
        "lightgbm",
        "bukmacherska",
        "bukmacherska_crystal"
    ],
    author="Twoje Imię",
    author_email="twojemail@example.com",
    description="Biblioteka łącząca funkcjonalności bukmacherska i bukmacherska_crystal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_repo/combined_bukmacherska",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
