from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setup(
    name="cltl.brain",
    description="The Leolani Brain module for knowledge representation",
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leolani/cltl-knowledgerepresentation",
    license='MIT License',
    authors={
        "Baez Santamaria": ("Selene Baez Santamaria", "s.baezsantamaria@vu.nl"),
        "Baier": ("Thomas Baier", "t.baier@vu.nl")
    },
    package_dir={'': 'src'},
    packages=find_namespace_packages(include=['cltl.*'], where='src'),
    package_data={'cltl.brain': ['ontologies/*', 'ontologies/**/*', 'queries/*', 'queries/**/*']},
    python_requires='>=3.7',
    install_requires=[
        # 'cltl.combot @ git+https://github.com/leolani/cltl-combot.git#e76f2baa4668d9546e93c7e5a5df102648d40c17',
        'requests>=2.25',
        'rdflib>=5.0',
        'sparqlwrapper>=1.8',
        'numpy>=1.20',
        'fuzzywuzzy>=0.18',
        'nltk>=3.4',
        'iribaker>=0.2',
        'rdflib-jsonld>=0.5',
        'python-Levenshtein>=0.12',
        'importlib_resources>=5.2'
    ],
    setup_requires=['flake8']
)
