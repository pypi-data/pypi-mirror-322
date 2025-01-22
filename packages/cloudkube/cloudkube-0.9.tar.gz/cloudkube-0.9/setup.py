from setuptools import setup, find_packages

setup(
    name="cloudkube",
    version="0.9",
    author="Chan Ming Han",
    email="chanminghan00@gmail.com",
    description="minikube for the cloud",
    python_requires=">=3.11",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cloudkube=cloudkube:main",
        ],
    },
    install_requires=[
        "boto3",
        "python_terraform",
        "kubernetes",
        "requests",
        "GitPython",
    ],
    package_data={"cloudkube": ["terraform/*"]},
)
