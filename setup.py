from setuptools import setup, find_packages

setup(
    name='asap',
    version='0.1.0',
    description='Auto Super-Auto-Pets: A simulated environment for Super Auto Pets with RL support',
    author='Dean Poulos',
    author_email='dean.poulos7@gmail.com',
    url='https://github.com/deanpoulos/ASAP',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'asap.ui': ['img/*']
    },
    install_requires=[
        'gym',
        'stable-baselines3',
        'Pillow',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'train_agent=asap.scripts.train_agent:main',
        ],
    },
)
