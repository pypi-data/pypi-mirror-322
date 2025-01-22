from setuptools import setup, find_packages

setup(
    name="weatheruz",
    version="0.6",  
    author="Axmadjon Qaxxorov",
    description="O'zbekistondagi obhavo malumotini olishingiz uchun kutubhona,Youtubedan @yukidevv obuna bo'ling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
