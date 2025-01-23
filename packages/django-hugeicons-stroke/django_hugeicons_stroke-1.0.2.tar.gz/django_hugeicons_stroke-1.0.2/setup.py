from setuptools import setup, find_packages

setup(
    name='django_hugeicons_stroke',
    version='1.0.2',
    description='A Django templatetag library for using hugeicons free stroke icons',
    url='',
    author='Kyvex',
    author_email='developer.gdean@proton.me',
    license='GPL',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'django_hugeicons_stroke': ['django_hugeicons_stroke/templatetags/hugeicons_stroke.py'],
    },
    include_package_data=True,
)
