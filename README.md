# cltl-knowledgerepresentation

A knowledge representation service (aka Leolani Brain). This service expects structures data and outputs an RDF graph.

### Description

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

## Installation

### Prerequisites

You will need to clone the [cltl-requirements](https://github.com/leolani/cltl-requirements.git) and
the [cltl-combot](https://github.com/leolani/cltl-combot.git) repositories. If you
checkout [cltl-combot](https://github.com/leolani/cltl-combot.git) including git submodules (that
adds [cltl-build](https://github.com/leolani/cltl-build) in the utils folder), you should be able to create a `dist/`
folder, in the [cltl-combot](https://github.com/leolani/cltl-combot.git) repository, containing the package.

```
git clone https://github.com/leolani/cltl-requirements.git
git clone https://github.com/leolani/cltl-combot.git
cd cltl-combot
git submodule update
make build
```

and then can nstall the package with just `pip install dist/cltl.combot-xxx.tar.gz` (see next section)

Additionally, you need to install [GraphDB](http://graphdb.ontotext.com/) with a repository named `leolani`. You will
need to launch this before running the package.

### Virtual environment

This repository uses Python >= 3.7.8 To set ip up you can run:

```bash
cd cltl-knowledgerepresentation
conda create --name cltl-knowledgerepresentation python=3.7
conda activate cltl-knowledgerepresentation
pip install <ABSOLUTE_PATH_TO_YOUR_COMBOT_REPO>/dist/cltl.combot-xxx.tar.gz
pip install -e .
```

### Test

Please take a look at the tests provided to get an idea on how to run and use this package. For these test, you need a
repository on GraphDB called `sandbox`

## To Do

- Fix logging