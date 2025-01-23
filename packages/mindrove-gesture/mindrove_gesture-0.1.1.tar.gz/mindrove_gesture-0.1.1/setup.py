from setuptools import setup, find_packages

setup(
    name='mindrove_gesture',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'scikit-learn',
        'tensorflow==2.12.0',
        'mindrove',
        "keyboard"
    ],
    entry_points={
        'console_scripts': [
            'record=mindrove_gesture.record:record_gestures',
            'fine_tune=mindrove_gesture.fine_tune:fine_tune_svm',
            'inference=mindrove_gesture.inference:real_time_inference',
        ]
    },
    author='MindRove',
    author_email='zsofia.budai@mindrove.com',
    description='A package for recording and analyzing gestures with MindRove.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/budzs/mindrove_gesture',
    package_data={"mindrove_gesture": ["data/*.h5", "data/*.pkl"]},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
