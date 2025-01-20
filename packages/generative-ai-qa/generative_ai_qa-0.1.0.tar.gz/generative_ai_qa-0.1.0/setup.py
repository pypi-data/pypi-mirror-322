from setuptools import setup, find_packages

setup(
    name="generative_ai_qa",
    version="0.1.0",
    description="A Python package for question answering using Google Generative AI.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Abhinav",
    author_email="abhinav.kumar@savatarr.tech",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.1.0"  # Ensure the dependency is correctly specified
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
