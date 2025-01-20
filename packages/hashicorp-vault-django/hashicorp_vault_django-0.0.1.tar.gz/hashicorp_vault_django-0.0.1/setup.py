import os
from setuptools import setup, find_packages

README = ""
readme_path = os.path.join(os.path.dirname(__file__), 'readme.md')
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        README = f.read()

setup(
    name='hashicorp_vault_django',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app to manage the application secrets using hashicorp.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/icedreamer-praveen/hashicorp-vault',
    author='icedreamer-praveen',
    author_email='prabinchy1234@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.10",
    extras_require={
        "dev": ['twine>=4.0.2',]
    }
)
