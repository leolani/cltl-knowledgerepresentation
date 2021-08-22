from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cltl.brain",
    description="The Leolani Brain module for knowledge representation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leolani/cltl-knowledgerepresentation",
    license='MIT License',
    authors={
        "Baez Santamaria": ("Selene Baez Santamaria", "s.baezsantamaria@vu.nl"),
        "Baier": ("Thomas Baier", "t.baier@vu.nl")
    },
    package_dir={'': 'src'},
    packages=find_namespace_packages(include=['cltl.*']),
    package_data={'brain': ['ontologies/*', 'queries/*']},
    python_requires='>=3.7', # downgraded python from 7.8 to 7 for my install, still works
    install_requires=[#'cltl.combot @ git+https://github.com/leolani/cltl-combot.git', # No need to install this anymore
                      'requests==2.25.0',
                      'rdflib==5.0.0',
                      'sparqlwrapper==1.8.5',
                      'numpy==1.20.0', #upgraded from 19.4 to 20.0 to make it compatible with emissor
                      'fuzzywuzzy==0.18.0',
                      'nltk==3.4.4',
                      'iribaker==0.2',
                      'rdflib-jsonld'
                      ],
    setup_requires=['flake8']
)
