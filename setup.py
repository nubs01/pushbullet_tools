import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as fh:
    long_description = fh.read()

requirementPath = os.path.join(here, 'requirements.txt')
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name='pushbullet_tools',
    version='0.0.5',
    author='Roshan Nanu',
    author_email='roshan.nanu@gmail.com',
    description='package for interacting with pushbullet via python',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/nubs01/pushbullet_tools',
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': [
            'pbmsg=pushbullet_tools.push_message:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'],
    keywords=('pushbullet pbmsg push message push_message alert code_alert '
              'push_alert notifications push_notification notify python '
              'package pushbullet_tools'),
    python_requires='>=3.6',
    install_requires=install_requires,
    include_package_data=True,
    package_data={}
)




