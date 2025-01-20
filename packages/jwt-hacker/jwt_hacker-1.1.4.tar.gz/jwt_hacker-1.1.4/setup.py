from setuptools import setup, find_packages

setup(
    name="jwt-hacker",
    version="1.1.4",  # Updated to reflect new features
    description="A futuristic tool to decode, analyze, and manipulate JWT tokens",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Z3r0 S3c",
    author_email="z3r0s3c@greynodesecurity.com",
    maintainer="Grey Node Security",
    maintainer_email="admin@greynodesecurity.com",
    url="https://github.com/GreyNodeSecurity/JWT_Hacker",
    project_urls={
        "Documentation": "https://github.com/GreyNodeSecurity/JWT_Hacker/wiki",
        "Source": "https://github.com/GreyNodeSecurity/JWT_Hacker",
        "Website": "https://greynodesecurity.com",
        "Tracker": "https://github.com/GreyNodeSecurity/JWT_Hacker/issues",
    },
    packages=find_packages(),  # Automatically discovers the packages
    include_package_data=True,  # Includes non-Python files specified in MANIFEST.in
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",  # Update based on the project's maturity
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="JWT decoding hacking security tool analysis manipulation",
    python_requires=">=3.6",
    install_requires=[
        "pycryptodome>=3.11.0",  # For cryptographic operations
        "pyjwt>=2.4.0",  # For JWT processing
        "cryptography>=39.0.0",  # For modern cryptographic primitives (Argon2, ECC, RSA, etc.)
        "requests>=2.20.0",  # For making HTTP requests
        "tkintertable",  # Optional: Extends tkinter table functionality
        "pytest>=7.0.0",  # For testing (optional if running tests in dev environment)
        "json",  # For JSON parsing (already included in Python, but listed for clarity)
        "datetime",  # For timezone handling (standard library, listed for clarity)
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],  # Development dependencies
    },
    entry_points={
        "console_scripts": [
            "jwthacker=jwt_hacker.gui:main",  # Expose the GUI tool
        ],
    },
    data_files=[
        ("docs", ["README.md", "LICENSE"]), # Include documentation files
        ("resources", ["resources/icon.ico", "resources/icon.icns", "resources/icon.png"]), 
    ],
    zip_safe=False,  # Set to False if the package cannot be reliably used from a .zip file
)
