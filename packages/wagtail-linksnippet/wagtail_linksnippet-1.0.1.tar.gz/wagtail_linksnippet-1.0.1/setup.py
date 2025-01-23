from setuptools import setup, find_packages

setup(
    name='wagtail_linksnippet',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Wagtail extension to open custom chooser from RichText Editor.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fabio Marras',
    author_email='fabio.marras@fintastico.com',
    url='https://github.com/fab10m/wagtail_linksnippet',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Wagtail',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'wagtail>=6.0',
        'django>=4.2'
    ],
    package_data={
        'wagtail_linksnippet': [
            'static/wagtail_linksnippet/js/modelChooser.js',
        ]
    },
    zip_safe=False,
)