from setuptools import setup, find_packages

setup(
    name="RedXSecurePayments",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "stripe>=7.0.0",
        "flask>=2.0.0"
    ],
    author="RedX",
    author_email="RedXDevelopment1998@gmail.com",
    description="A flexible and secure payment collection system using Stripe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/RedXSecurePayments/",
    project_urls={
        "Repository": "https://github.com/RedXSecurePayments/RedXSecurePayments",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False
)