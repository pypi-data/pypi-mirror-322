from setuptools import setup, find_packages

setup(
    name="tw_django_base_library",
    version="1.2.2",
    author="Rohit Hazare",
    author_email="rohit@techwalnut.com",
    description="A library for setting up a django project according to Techwalnut innovations LLP guidelines",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dev2_techwalnut/tw-django-base-library.git",  # GitHub repo link
    packages=find_packages(),
    include_package_data=True,  # Include static files, templates, etc.
    install_requires=[
        "Django>=4.2",  # Specify the minimum Django version
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
