from setuptools import setup

setup(
    name='pseudo',
    version='0.2.6',
    description='a framework for high level code generation',
    author='Alexander Ivanov',
    author_email='alehander42@gmail.com',
    url='https://github.com/alehander42/pseudo',
    download_url='https://github.com/alehander42/pseudo/archive/v0.2.tar.gz',
    keywords=['compiler', 'generation', 'c++', 'ruby', 'c#', 'javascript', 'go', 'python', 'alexander'],
    packages=['pseudo', 'pseudo.api_translators', 'pseudo.middlewares', 'pseudo.generators'],
    license='MIT',
    install_requires=[
        'PyYAML'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'pseudo=pseudo.main:main',
        ],
    },
)
