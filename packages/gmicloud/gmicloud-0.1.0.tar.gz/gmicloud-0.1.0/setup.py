from setuptools import setup, find_packages

setup(
    name='gmicloud',
    version='0.1.0',
    author='GMI',
    author_email='gmi@gmitec.net',
    description='GMI Cloud Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GMISWE/python-sdk',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'openai',
        'requests',
        'pydantic',
        'httpx',
        'PyJWT',

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
