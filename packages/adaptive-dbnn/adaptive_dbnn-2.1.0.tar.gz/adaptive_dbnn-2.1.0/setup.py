# setup.py
from setuptools import setup, find_packages

setup(
    name="adaptive-dbnn",
    version="2.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.13.0",
        "torchvision>=0.14.0",
        "pandas>=1.4.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "tqdm>=4.62.0",
        "requests>=2.26.0",
        "pynput>=1.7.0",
        "python-xlib>=0.31; platform_system=='Linux'"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    author="Ninan Sajeeth Philip",
    author_email="nsp@airis4d.com",
    description="Adaptive Deep Bayesian Neural Network Implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sajeethphilip/adaptive-dbnn",
)