from setuptools import setup, find_packages

setup(
    name="bukmacherska_crystal",
    version="0.1.0",  # Wersja 0.1.0
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "pandas",
        "lightgbm",
        "bukmacherska"
    ],
    author="Twoje Imię",
    author_email="twojemail@example.com",
    description="Biblioteka do przewidywania wyników różnych zdarzeń w meczach piłkarskich",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_repo/bukmacherska_crystal",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
