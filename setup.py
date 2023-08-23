from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="hotel-booking-fastapi",
    packages=find_packages(),
    python_requires=">=3.11.3",
    install_requires=requirements
)
