from setuptools import setup, find_packages

setup(
    name='python_PixelArt',
    version='0.3.3',
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "numpy"
    ],
    author='Léonor Leclerc',
    author_email='leo-nor7777@outlook.com',
    description='Une bibliothèque qui fait des Pixel Arts. / A library that makes Pixel Arts.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5'
)
