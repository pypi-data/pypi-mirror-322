from setuptools import setup, find_packages

setup(
    name="audio_processor_GovGPT",
    version="0.1.0",
    author="Soumyajit Sen Sharma",
    author_email="soumyajit94298@gmial.com",
    description="A library to remove silence from audio files using pydub.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='',
    packages=find_packages(),
    install_requires=[
        "pydub",  # Add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
