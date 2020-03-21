from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="massspring",
    packages=["massspring"],
    version='0.0.5',
    license='MIT',
    description='A better mass-spring real world simulator with new types of forces(gravity, electricity, spring, collision, ...)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Pooya Shams kolahi',
    author_email='pooya.shams.k@gmail.com',
    url='https://github.com/pooya-shams/massspring',
    download_url='https://github.com/pooya-shams/massspring/archive/v0.0.5.tar.gz',
    keywords=["physics",
              "physics-3d",
              "physics-simulation",
              "mass-spring",
              "mass-spring-simulation",
              "python",
              ],
    install_requires=[
        "pygame",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
