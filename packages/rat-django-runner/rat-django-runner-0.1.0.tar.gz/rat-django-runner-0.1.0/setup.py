from setuptools import setup, find_packages

setup(
    name="rat-django-runner",
    version="0.1.0",
    packages=find_packages(),
    description="Django runserver uchun IP va portni oson boshqarish kutubxonasi",
    author="Sharifjom Mo'minov",
    author_email="mominovsharif@gmail.com",
    url="https://github.com/sharifjon/rat",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
