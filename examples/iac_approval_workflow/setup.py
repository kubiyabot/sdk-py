from setuptools import setup, find_packages

setup(
    name="kubiya_iac_approval",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["kubiya", "pydantic", "pytimeparse", "litellm", "boto3"],
    # entry_points={
    # 'console_scripts': [
    #     'kubiya=kubiya.cli:main',
    # ],
    # },
)
