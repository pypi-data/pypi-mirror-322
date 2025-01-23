from setuptools import setup, find_packages

setup(
    name="behavioral_biometrics",  
    version="0.1.1",  
    packages=find_packages(), 
    description="A Python package that can be used for behavioral anomaly",  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    author="Your Name",  
    author_email="your.email@example.com",  
    url="https://github.com/yourusername/hash_generator", 
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",  
    ],
    python_requires='>=3.8',
    install_requires=[],
    include_package_data=False,
    package_data={  
        '': ['README.md', 'LICENSE'], 
    },
)
