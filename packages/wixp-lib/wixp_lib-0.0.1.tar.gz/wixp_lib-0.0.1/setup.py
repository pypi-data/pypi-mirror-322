from setuptools import setup, find_packages

setup(
    name='wixp_lib',
    version='0.0.1',
    description='Created for convenience',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dmitriy Bobkov/WiXP Dev',
    author_email='dimabobkov2016@gmail.com',
    url='https://github.com/DcorpProj/wixp_lib',  # URL на ваш репозиторий
    packages=find_packages(),
    install_requires=[         # Зависимости
        'rich',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Лицензия
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
