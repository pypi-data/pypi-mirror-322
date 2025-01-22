from setuptools import setup, find_packages

desc = '\n'.join(("Универсальная библиотека python для большинства задач", 'A universal python library for most tasks'))
req = open('requirements.txt').read().split('\n')


def long_desc():
    eng = open('README.md').read()
    ru = open('README_RU.md', encoding='utf-8').read()
    sep = '''
-----------------------------------------
    '''
    return sep.join((eng, ru))


setup(
    name='hrenpack',
    version='1.1.0',
    author_email='hrenpack@mail.ru',
    author='Маг Ильяс DOMA (MagIlyas_DOMA)',
    description=desc,
    license='BSD 3-Clause License',
    long_description=long_desc(),
    long_description_content_type='text/markdown',
    url='https://github.com/MagIlyas-DOMA/hrenpack',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=req,
    package_data={'hrenpack': ['hrenpack/resources/*']},
    include_package_data=True,
)
