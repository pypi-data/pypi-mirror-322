
from setuptools import setup , find_packages

setup(
    name="QudimiStructLib",
    version="0.3",
    author="Abdulaziz AL-qudimi",
    author_email="eng7mi@gmail.com",
    description="Data Structures",
    packages=find_packages(),
    install_requires=["matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_reuires=">=3.6",
    )
