from setuptools import setup, find_packages

setup(
    name='modulus-ml',
    version='0.1.0',
    description='A library for comparing and evaluating ML models',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Akinsanya Joel',
    author_email='akinsanyajoel82@gmail.com',
    url='https://github.com/kiojoel/modulus-ml',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'numpy',
        'pandas',
        'matplotlib'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
