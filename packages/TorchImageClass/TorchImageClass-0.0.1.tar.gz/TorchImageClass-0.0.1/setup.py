from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TorchImageClass",
    version="0.0.1",
    author="Diogo Ribeiro",
    author_email="diogoifroads@gmail.com",
    description="A library for image classification using PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiogoBrazil/lib-to-class-image-with-pytorch.git",
    packages=find_packages(),
    license="MIT",
    keywords=[
        "pytorch",
        "deep-learning",
        "image-classification",
        "machine-learning",
        "computer-vision",
        "classification",
        "torch",
        "TorchImageClass",
        "neural-networks",
        "cnn",
        "transfer-learning"
    ],
    install_requires=[
        "torch",
        "torchvision",
        "torchmetrics",
        "tqdm",
        "Pillow",
    ],
    python_requires=">=3.9",
)
