from setuptools import setup

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='json-direct',
    version='1.0.1',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/json-direct',
    description='Overwrite the default behavior of json.dumps to ensure_ascii=False',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['json_direct'],
    python_requires='>=3.6',
    platforms=["all"],
    license='MIT'
)
