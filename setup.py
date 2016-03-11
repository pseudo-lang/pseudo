from distutils.core import setup

setup(
    name='pseudo',
    version='0.2',
    description='a framework for high level code generation',
    author='Alexander Ivanov',
    author_email='alehander42@gmail.com',
    url='https://github.com/alehander42/pseudo',
    download_url='https://github.com/alehander42/pseudo/tarball/0.2',
    keywords=['compiler', 'generation', 'c++', 'ruby', 'c#', 'javascript', 'go', 'python', 'transpiler'],
    packages=['pseudo'],
    license='MIT License',
    install_requires=[
        'PyYAML==3.11'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: JavaScipt'
    ],
)
