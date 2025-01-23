from setuptools import setup
setup(
	name='django_hugeicons_stroke',
	version='1.0.1',
	description='A Django templatetag library for using hugeicons free stroke icons',
	url='',
	author='Kyvex',
	author_email='developer.gdean@proton.me',
	license='GPL',
	packages=['django_hugeicons_stroke'],
	zip_safe=False,
	data_files=[
		('templatetags', ['django_hugeicons_stroke/templatetags/hugeicons_stroke.py']),
	],
)