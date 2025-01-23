from setuptools import setup
 
setup(
    name='showast2',
    packages=['showast2', 'showast2.rendering', 'showast2.util',],
    version='0.3.2',
    description = 'IPython notebook plugin for visualizing abstract syntax trees. Unofficial update for Python >= 3.12 by Andreas Zeller.',
    license='MIT',
    author='H. Chase Stevens',
    author_email='chase@chasestevens.com',
    url='https://github.com/hchasestevens/show_ast',
    install_requires=[
        'ipython',
        'graphviz',
    ],
    extras_require={
        'nltk': ['nltk', 'pillow'],
    },
    keywords='ipython jupyter notebook ast asts graphing visualization syntax',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Code Generators',
        'Framework :: IPython',
        'Topic :: Multimedia :: Graphics :: Presentation',
    ]
)
