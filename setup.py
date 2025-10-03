from setuptools import setup, find_packages

setup(
    name="growbox",
    version="1.0.0",
    description="GrowBox IoT Control System - Environmental monitoring and automation for indoor plant cultivation",
    author="GrowBox Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "paho-mqtt>=1.6.1",
        "Jetson.GPIO>=2.1.6",
        "Flask>=2.3.3",
        "Flask-SocketIO>=5.3.4",
        "python-socketio>=5.9.0",
        "Adafruit-DHT>=1.4.0",
        "smbus2>=0.4.2",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "jsonschema>=4.19.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "growbox=main:main",
        ],
    },
)
