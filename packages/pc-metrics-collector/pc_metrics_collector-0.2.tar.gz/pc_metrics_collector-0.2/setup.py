from setuptools import setup, find_packages

setup(
    name='pc_metrics_collector',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'websockets',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'pc_metrics_collector=DeskPerformance.pf:main',
        ],
    },
)