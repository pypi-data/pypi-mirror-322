import os
from setuptools import setup, find_packages

# Get CUDA version from the env variable, defaulting to '11.6' if not set
cuda_version = os.getenv('CUDA_VERSION', '12.1')

# Strip the period from the version string (e.g., '11.6' -> '116')
cuda_version = cuda_version.replace('.', '')

# Format version to get prebuilt wheel
cupy_package = f'cupy-cuda{cuda_version}'

setup(
    name='oct_tissuemasking',
    version='0.0.8',
    description='A PyTorch based package for automated OCT tissue masking.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Etienne Chollet',
    author_email='etiennepchollet@gmail.com',
    url='https://github.com/EtienneChollet/oct_tissuemasking',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'oct_tissuemasking=oct_tissuemasking:app'
            ]
        },
    install_requires=[
        'torch',
        'torchvision',
        'torchaudio',
        'torchmetrics',
        'nibabel',
        'matplotlib',
        'tensorboard',
        'cornucopia',
        'cyclopts'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='~=3.9',
    include_package_data=True,
    package_data={
        'oct_tissuemasking': ['checkpoints/*'],
    },
)
