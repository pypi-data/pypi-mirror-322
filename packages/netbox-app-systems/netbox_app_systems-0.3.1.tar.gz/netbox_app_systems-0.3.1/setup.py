from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='netbox_app_systems',
    version='0.3.1',
    description='Netbox plugin. Assign devices and virtual machines to application systems',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['drf_yasg'],
    download_url='https://pypi.org/project/netbox-app-systems/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['netbox', 'netbox-plugin'],
    author='Oleg Senchenko',
    author_email='senchenkoob@mail.ru',
    maintainer='Oleg Senchenko',
    maintainer_email='senchenkoob@mail.ru',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
