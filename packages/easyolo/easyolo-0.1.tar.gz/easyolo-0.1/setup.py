# setup.py

from setuptools import setup, find_packages

setup(
    name='easyolo',
    version='0.1',
    packages=find_packages(),
    description='A Simple YOLO Implementation for Object Detection',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='AKM Korishee Apurbo',
    author_email='bandinvisible8@gmail.com',
    url='https://github.com/IMApurbo/easyolo',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'ultralytics>=8.0.0',  # For YOLOv5
        'opencv-python>=4.5.0',  # For image processing
        'torch>=1.7.0',  # For PyTorch (if using YOLOv5 with PyTorch)
        'scikit-learn>=0.24.0',  # For any utility or ML features (optional)
        'pillow>=8.0.0',  # For image manipulation (optional)
    ],
    python_requires='>=3.6',  # Specify the minimum required Python version
    include_package_data=True,
)
