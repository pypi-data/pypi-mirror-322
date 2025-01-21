from setuptools import setup, find_packages

setup(
    name='UnleashSDK',
    version='1.0.0',
    packages=find_packages(),
    license='GNU General Public License v3.0',
    description='A python wrapper for the Unleash Nfts API',
    long_description=open('README.md').read(),
    install_requires=[
        'requests',
    ],
    url='https://github.com/kbm9696/Unleash-SDK',
    author='Balamurugan',
    author_email='balamurugankarikalan.96@gmail.com',
    long_description_content_type='text/markdown'
)
