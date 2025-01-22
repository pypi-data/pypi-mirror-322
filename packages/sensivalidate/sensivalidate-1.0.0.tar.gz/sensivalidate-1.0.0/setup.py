from setuptools import setup

setup(
    name="sensivalidate",
    version="1.0.0",
    package_dir={
        "": "src",
        "sensivalidate": "src/sensivalidate_rootifera"
    },
    packages=["sensivalidate"],
    install_requires=[
        'creditcard==1.0.2',
    ],
    description="A module to find credit card, UK bank account, sort code and postcode in text",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Omur Ozbahceliler",
    author_email="omur@rootifera.org",
    url="https://github.com/rootifera/sensivalidate",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)