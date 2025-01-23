from setuptools import setup, find_packages
import os

# Читаем содержимое README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='d1_library',
    version='1.0.0',
    description='D-one Trading Platform Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='D-one',
    author_email='your.email@example.com',  # Добавьте ваш email
    url='https://github.com/reraaaaa/D-one-Trading-Platform',  # URL вашего репозитория
    packages=find_packages(include=['d1_library', 'd1_library.*']),
    include_package_data=True,
    python_requires='>=3.8,<3.13',
    install_requires=[
        'numpy>=1.26.0',
        'pandas>=2.1.0',
        'pytz>=2022.6',
        'requests>=2.31.0',
        'scipy>=1.11.0',
        'SQLAlchemy>=1.4.44',
        'fmp-python>=0.1.4',
        'cvxpy>=1.4.2',
        'yfinance>=0.2.33',
        'PyPortfolioOpt>=1.5.5',
        'alpha_vantage>=2.3.1',
        'psycopg2-binary>=2.9.5',
        'python-dotenv>=0.19.0',
        'ib-insync>=0.9.86'
    ],
    package_data={
        'd1_library': [
            'sql_tools/sql_scripts/*.sql',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
