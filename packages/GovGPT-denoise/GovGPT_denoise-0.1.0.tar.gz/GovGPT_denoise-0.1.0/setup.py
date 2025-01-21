from setuptools import setup, find_packages

setup(
    name="GovGPT_denoise",
    version="0.1.0",
    description="A simple and short denoising algorithm to denoise maximum amount of noise from an audio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Soumyajit Sen Sharma",
    author_email="soumyajit94298@gmail.com",
    url='',
    packages=find_packages(),
    install_requires=[
        "soundfile",
        "noisereduce",
        "torchaudio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
