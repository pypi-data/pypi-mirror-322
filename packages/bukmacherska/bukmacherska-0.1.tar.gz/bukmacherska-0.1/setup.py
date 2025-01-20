from setuptools import setup, find_packages

setup(
    name='bukmacherska',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
    ],
    author='Twoje Imię',
    author_email='twojemail@example.com',
    description='Biblioteka do obliczeń bukmacherskich',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/twoje_konto/bukmacherska',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
