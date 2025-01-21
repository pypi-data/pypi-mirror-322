from setuptools import find_packages, setup

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ipmt',  # Library name
    version='0.1.3',  # Version
    author='night9a',  # Your name
    author_email='nightxcros@gmail.com',  # Your email
    description=(
        'A Flask-based IP management dependency that helps manage IP '
        'addresses, monitor visitors, and protect websites from DDoS attacks.'
    ),
    long_description=long_description,  # Use README for detailed description
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find packages
    install_requires=[
        'Flask>=2.0', 
        'Flask-Limiter>=2.0',
    ],
    setup_requires=['wheel'],  # For building the distribution
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Flask',
    ],
    python_requires='>=3.7',  # Minimum Python version
)
