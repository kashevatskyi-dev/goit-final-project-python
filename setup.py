from setuptools import setup, find_packages

setup(
    name='keeply',
    version='1.0.0',
    description='Personal Assistant CLI App for managing contacts and notes.',
    author='Group-5',
    packages=find_packages(),
		install_requires=[
        'tabulate',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            # Цей рядок означає: при введенні команди keeply в терміналі, 
            # запусти функцію main() з файлу main.py у пакеті keeply
            'keeply = keeply.main:main',
        ],
    },
)