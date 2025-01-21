from setuptools import setup, find_packages

setup(
    name="nnaudio_GovGPT",
    version="0.1.0",
    description="A library for optimizing audio processing parameters using differential evolution.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Soumyajit Sen Sharma",
    author_email="soumyajit94298@gmal.com",
    url='',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "librosa",
        "noisereduce",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
