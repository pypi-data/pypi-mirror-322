from setuptools import setup, find_packages

setup(
    name='dungeon-crawler',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pygame==2.6.1',
        'opencv-python==4.10.0.84',
        'mediapipe==0.10.18',
        'numpy==1.26.4',
        #Add other dependencies here if needed
    ],
    entry_points={
        'console_scripts': [
            'dungeon-crawler=main:main',
        ],
    },
    author='Kamil Kras, Mateusz Purol, Konrad Włodarczyk',
    author_email='mateuszpurol@student.agh.edu.pl',
    description='A hand gesture-controlled dungeon-crawler game',
    url='https://design-lab.agh.zymon.org/design-lab/dungeon-crawler',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
