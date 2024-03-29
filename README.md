# cltl-knowledgerepresentation

A knowledge representation service (aka Leolani's Brain). This service expects structures data and outputs an RDF graph.

## Description

This package contains the necessary functionality for creating an RDF episodic knowledge graph. It features:

- Representation of experiences and their context
- Storing of learned facts, their mentions/references, and the perspectives expressed
- Querying of the graph as a way of accessing memories created during previous experiences
- Typing of incoming information through querying of external knowledge sources like DBpedia and Wikidata
- Location reasoning for guessing where a new experience is taking place, based on previous locations
- Thoughts and drives that arise from new information added to the graph. For example
    - conflicts resulting from learned facts,
    - curiosity based on knowledge gaps,
    - generalization via shared characteristics across people or objects
- Trust calculation of agents as sources of information. The trust value is based on:
    - the number of interaction with this agent,
    - the number of new content the agent has provided,
    - the number of conflicting information it has provided

## Getting started

### Prerequisites

This repository uses Python >= 3.7

Be sure to run in a virtual python environment (e.g. conda, venv, mkvirtualenv, etc.)

### Installation

1. In the root directory of this repo run

    ```bash
    pip install -e .
    python -c "import nltk; nltk.download('wordnet')"
    ```

2. Additionally, you need to install [GraphDB Free](http://graphdb.ontotext.com/) with a repository named `sandbox`. You
   will need to launch this before running the package.

### Usage

For using this repository as a package for different project and on a different virtual environment, you may

- install a published version from PyPI:

    ```bash
    pip install cltl.brain
    ```

- or, for the latest snapshot, run:

    ```bash
    pip install git+git://github.com/leolani/cltl-knowledgerepresentation.git@main
    ```

Then you can import it in a python script as:

    import cltl.brain


You can also modify the logger level as such:

```python
import logging

from cltl.brain import logger as brain_logger

brain_logger.setLevel(logging.ERROR)
```
## Examples

Please take a look at the example scripts provided to get an idea on how to run and use this package. Each example has a
comment at the top of the script describing the behaviour of the script.

For these example scripts, you need

1. A repository on [GraphDB Free](http://graphdb.ontotext.com/) called `sandbox`. To run any example script you first
   have to launch GraphDB, and then you can run the example script.

2. To change your current directory to `./examples/`

3. Run some examples (e.g. `python carl.py`)


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License.
See [`LICENSE`](https://github.com/leolani/cltl-knowledgerepresentation/blob/main/LICENCE) for more information.

## Authors

* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
* [Piek Vossen](https://github.com/piekvossen)