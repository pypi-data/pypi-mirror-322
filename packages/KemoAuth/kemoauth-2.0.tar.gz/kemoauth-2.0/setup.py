from setuptools import setup, find_packages

setup(
    name="KemoAuth",
    py_modules=["KemoAuth"],
    version="2.0",
    packages=find_packages(),
    description="Kemoauth is a Simple Key System",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="DewzaCSharp",
    author_email="dewzacsharp@gmail.com",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["setuptools", "wheel", "asyncio", "typing", "psutil", "uuid"],  # Abhängigkeiten hier einfügen, wenn nötig
)
