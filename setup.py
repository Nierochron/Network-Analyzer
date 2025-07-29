from setuptools import setup, find_packages

setup(
    name='network-analyzer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple network analyzer that scans nearby networks and collects SSID, signal strength, and MAC addresses.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'scapy',
        'pywifi',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)