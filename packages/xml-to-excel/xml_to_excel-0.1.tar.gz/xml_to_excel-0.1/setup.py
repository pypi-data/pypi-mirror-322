from setuptools import setup, find_packages

setup(
    name='xml_to_excel',  # Package name
    version='0.1',        # Version number
    packages=find_packages(),  # This will automatically find the package
    install_requires=['openpyxl'],  # Dependencies
    author='Yagna',
    author_email='yagna781@gmail.com',
    description='A utility for converting XML files to Excel',
    #long_description=open('README.md').read(),  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/yourusername/xml_to_excel',  # Optional
    classifiers=[  # Optional but helps with categorizing
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Optional, specify Python versions
)

