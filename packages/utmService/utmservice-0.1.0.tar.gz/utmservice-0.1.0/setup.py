from setuptools import setup, find_packages

setup(
    name="utmService",  
    version="0.1.0",  
    author="Ravi Ashok Pashchapur",
    author_email="ravi.pashchapur@tii.ae",
    description="A Python library for UTM services",
    url="https://github.com/tiiuae/drone_ussp_svc",  
    packages=find_packages(),  
    include_package_data=True,
    install_requires=[
        "configparser",
        "pyserial",
        "flask",
        "flask-cors",
        "paho-mqtt",
        "pynmeagps",
        "pyopenssl",
        "cryptography",
        "requests"  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",  
)
