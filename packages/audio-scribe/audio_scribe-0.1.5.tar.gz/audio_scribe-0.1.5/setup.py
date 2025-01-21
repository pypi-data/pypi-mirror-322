import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio_scribe",
    version="0.1.5",
    author="Gurasis Osahan",
    author_email="contact@genomicops.com",
    description="A command-line tool for audio transcription with Whisper and Pyannote.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.genomicops.cloud/genomicops/audio-scribe",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "torch",
        "openai-whisper",
        "pyannote.audio",
        "pytorch-lightning",
        "keyring",
        "cryptography",
        "alive-progress",
        "psutil",
        "GPUtil",
    ],
    entry_points={"console_scripts": ["audio-scribe=audio_scribe.transcriber:main"]},
    keywords="whisper pyannote transcription audio diarization",
    license="Apache-2.0",
    project_urls={
        "Source": "https://gitlab.genomicops.cloud/genomicops/audio-scribe",
        "Tracker": "https://gitlab.genomicops.cloud/genomicops/audio-scribe/-/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
