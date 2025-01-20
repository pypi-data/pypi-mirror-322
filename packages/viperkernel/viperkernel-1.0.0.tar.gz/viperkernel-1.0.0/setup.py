import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="viperkernel",
    version="1.0.0",
    author="Alexander L.E. Wang",
    author_email="aw3436@cumc.columbia.edu",
    packages=["viperkernel"],
    description="A package to perform VIPER-based velocity in Python",
    long_description="This Cellrank-compatible package provides the ability to use VIPER protein activity to create a kernel and infer transformation of cell states..",
    long_description_content_type="text/markdown",
    url="https://github.com/alexanderlewis99/VIPERKernel/",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        "cellrank",
        "tqdm",
        "numpy"
    ]
)
