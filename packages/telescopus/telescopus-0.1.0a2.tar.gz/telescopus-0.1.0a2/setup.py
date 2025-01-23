import os
import sys
import platform
from setuptools import setup

# Determine the Python version
python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"

# Determine the platform and architecture
platform_system = platform.system().lower()  # 'windows', 'linux', 'darwin'
platform_arch = platform.machine().lower()   # 'amd64', 'x86_64', etc.

if platform_system == "windows":
    binary_extension = f".{python_version}-win_{platform_arch}.pyd"
elif platform_system == "linux":
    binary_extension = f".{python_version}-linux_{platform_arch}.so"
elif platform_system == "darwin":  # macOS
    binary_extension = f".{python_version}-macos_{platform_arch}.so"
else:
    raise RuntimeError("Unsupported platform!")

# Full binary name
binary_name = f"telescopus{binary_extension}"

binary_path = os.path.join("telescopus", "binaries", binary_name)
if not os.path.exists(binary_path):
    raise RuntimeError(f"No pre-built binary available for {binary_name} (binary_path: {binary_path}, binary_extension: {binary_extension})")

setup(
    name="telescopus",
    version="0.1.0a2",
    description="A Python profiler with a rich UI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Softanics",
    url="https://www.softanics.com/python/profiler/",
    packages=["telescopus"],
    package_data={"telescopus": [f"binaries/{binary_name}"]},
    license="Proprietary",
    license_files=["LICENSE"],
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7", #todo
)
