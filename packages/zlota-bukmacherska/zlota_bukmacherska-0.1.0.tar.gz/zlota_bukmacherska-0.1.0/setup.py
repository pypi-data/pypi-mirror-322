from setuptools import setup, find_packages

setup(
    name="zlota_bukmacherska",
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
        "stalowa_bukmacherska"
    ],
    author="Twoje Imię",
    author_email="twojemail@example.com",
    description="Biblioteka do przewidywania correct score i typów zakładów",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/twoj_repo/zlota_bukmacherska",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
