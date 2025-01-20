from setuptools import setup, find_packages

setup(
    name='hollow',
    version='0.1.0',
    author="Tianyi Ma",
    author_email="tym.andy777@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Andy-0x0/Hollow-Knight-Save-Editor-CLI",
    license="GPL-3.0",
    description="Hollow Knight Save Modifier CLI",
    python_requires='>=3.7',
    
    install_requires=[
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'hollow = hollow.cli:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
