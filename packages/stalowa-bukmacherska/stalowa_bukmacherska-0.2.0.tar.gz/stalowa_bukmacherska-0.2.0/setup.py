from setuptools import setup, find_packages

setup(
    name="stalowa_bukmacherska",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "kivy",
        "pandas",
        "lightgbm"
    ],
    author="Twoje Imię",
    author_email="twojemail@example.com",
    description="Biblioteka do obliczania liczby goli",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_repo/stalowa_bukmacherska",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
