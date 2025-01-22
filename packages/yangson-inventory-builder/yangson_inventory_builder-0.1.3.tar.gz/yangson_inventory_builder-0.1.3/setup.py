from setuptools import setup, find_packages

setup(
    name='yangson_inventory_builder',
    version="0.1.3",
    description="Building inventory for the Yangson Python tool",
    author="Dmitrii Khorn",
    author_email="dima.khorn@gmail.com",
    packages=find_packages(),
    install_requires=[
        'annotated-types==0.7.0',
        'pydantic==2.5.3',
        'pydantic_core==2.14.6',
        'typing_extensions==4.12.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
