from setuptools import setup, find_packages

setup(
    name='myvenv',  # PyPI package name (must be unique if published publicly)
    version='0.1.0',
    description='A simple Windows utility to create or activate a Python virtual environment in the current CMD shell.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='ILikeAI',
    author_email='joshlikesai@gmail.com',
    url='https://github.com/ILikeAI/myvenv',  # Update with your repo if public
    license='MIT',
    packages=find_packages(),
    scripts=['myvenv.bat'],  # The key line: install our batch file into Scripts/
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
    ],
)
