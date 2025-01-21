from setuptools import setup, find_packages

setup(
    name="demoscms",  # The name of your library
    version="0.1",  # Version of your library
    packages=find_packages(),  # Automatically find packages
    description="A simple CMS for demos",  # Short description
    long_description=open('README.md').read(),  # Read long description from README.md
    long_description_content_type='text/markdown',  # Markdown format
    author="BHUSAHN SANJAY AZDE",  # Your name
    author_email="bhushanzade02@gmail.com",  # Your email
    url="https://github.com/bhushanzade02/demoscms",  # URL for your project (replace with actual)
    classifiers=[  # Classifiers to categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version required
)
 
