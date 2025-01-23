from setuptools import setup, find_packages

setup(
    name='groclake',  # Name of the package
    version='0.2.0',
    packages=find_packages(),
    namespace_packages=['groclake'],  # Declare the namespace
    install_requires=['requests', 'mysql-connector-python', 'redis', 'elasticsearch>=8.11.0,<9.0.0'],  # Add external dependencies if any
)

