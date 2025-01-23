from setuptools import setup, find_packages

setup(
    name='django_hugeicons_stroke',
    version='1.0.7',
    description='A Django templatetag library for using hugeicons free stroke icons',
    url='',
    author='Kyvex',
    author_email='developer.gdean@proton.me',
    license='GPL',
    packages=find_packages(include=['django_hugeicons_stroke', 'django_hugeicons_stroke.*']),  # ✅ Includes all submodules
    zip_safe=False,
    package_data={
        'django_hugeicons_stroke': ['templatetags/*.py'],  # ✅ Ensures templatetags is included
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=['Django>=3.0'],
    python_requires='>=3.6',
)
