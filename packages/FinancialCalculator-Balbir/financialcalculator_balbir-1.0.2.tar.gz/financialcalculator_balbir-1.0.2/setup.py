from setuptools import setup, find_packages

setup(
    name='FinancialCalculator-Balbir',
    version='1.0.2',  # Make sure this is incremented if it’s a re-upload
    author='Balbir SIngh Bhatia',
    author_email='balbirs2204@gmail.com',
    description='A Python package for financial calculations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/your-repo',  # Update this accordingly
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
