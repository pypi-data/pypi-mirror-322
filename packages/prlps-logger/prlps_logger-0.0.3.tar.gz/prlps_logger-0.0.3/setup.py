from setuptools import setup, find_packages

setup(
    name='prlps_logger',
    version='0.0.3',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/gniloyprolaps/prlps_logger',
    license='LICENSE.txt',
    description='простой пример логгера для записи логов в файл и вывода в консоль, или в html для HTMLResponse FastAPI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[

    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Education :: Testing',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Logging',
    ],
)
