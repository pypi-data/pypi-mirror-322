from setuptools import setup, find_packages, Extension

setup(
    name='bnapy',
    version='0.1',
    description='Bipartite Network Analysis',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://bnapy.readthedocs.io/en/latest/index.html',
    author='Baiyue He, Alec Kirkley, Shihui Feng',
    author_email='baiyue.he@connect.hku.hk, akirkley@hku.hk, shihuife@hku.hk',
    license='The MIT License',
    project_urls={
        "Documentation": "https://bnapy.readthedocs.io/en/latest/index.html",
        "Source": "https://bnapy.readthedocs.io/en/latest/index.html"
    },
    python_requires=">=3.9, <3.12",
    install_requires=[
        "numpy>=1.24",    
        "pandas>=2.2",
        "scipy>=1.10",
        "scikit-network>=0.33"
    ],
    packages=find_packages(),
    include_package_data=True,
)
