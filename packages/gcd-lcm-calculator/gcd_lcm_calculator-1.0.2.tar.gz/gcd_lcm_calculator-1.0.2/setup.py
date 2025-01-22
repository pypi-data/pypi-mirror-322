from setuptools import setup
import os

setup(
    name="gcd-lcm-calculator",  # Projenizin adı (benzersiz olmalı)
    version="1.0.2",  # Versiyon numarası
    author="Burak Cantürk",
    author_email="burakcanturk12@gmail.com",
    description="You can find the gcm (greatest common divisior) and lcm (least command multiplier) of the numbers. And also you can find the other values of the primity.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/burakcanturk/Quectel-5G-LTE-Module-Library.git",
    packages=["gcdlcm"],
    install_requires=[],  # Eğer dış bağımlılıklar varsa buraya ekleyin
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)