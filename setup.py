from setuptools import setup

setup(
    name='camperapp',
    packages=['camperapp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
