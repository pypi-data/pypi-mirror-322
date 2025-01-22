from setuptools import setup, find_packages
import os

def read_long_description():
    """Helper function to read the content of README.md"""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()
setup(
    name="perceptionpro",
    version="0.1.2",
    packages=find_packages(include=['perceptionpro', 'perceptionpro.*']),
    install_requires=[
        'opencv-python',
        'mediapipe',
        'ultralytics',
        'opencv-python-headless',
        'numpy'
    ],
    author="Umar Balak",
    author_email="umarbalak35@gmail.com",
    description="PerceptionPro is a package for computer vision tasks such as head pose estimation, eye tracking, and object detection.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
