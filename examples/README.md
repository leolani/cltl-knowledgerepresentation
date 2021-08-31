## Examples

Please take a look at the example scripts provided to get an idea on how to run and use this package. Each example has a
comment at the top of the script describing the behaviour of the script.

For these example scripts, you need

1. Setup a repository on [GraphDB Free](http://graphdb.ontotext.com/) called `sandbox`. To run any example script you first
   have to launch GraphDB, and then you can run the example script.

1. Install the package. It is recommended to do this in a virtual environment:
   ```shell
       > python -m venv examples/venv
       > source examples/venv/bin/activate
       (venv) > pip install .
   ```
   To exit and clean the virtual environment after use run
   ```shell
       (venv) > deactivate
       > rm -rf examples/venv
   ```

1. Change your current directory to `./examples/`

1. Run some examples (e.g. `python carl.py`)

### Capsules

'Capsules' are the way in which this package expects information for processing. They are `JSON` structures (or `JSON`
-like objects like Python dictionaries) in the following format:

```python

{
    "chat": 1,
    "turn": 1,
    "author": "carl",
    "utterance": "I need to take my pills, but I cannot find them.",
    "utterance_type": UtteranceType.STATEMENT,
    "position": "0-25",
    "subject": {"label": "carl", "type": "person"},
    "predicate": {"type": "see"},
    "object": {"label": "pills", "type": "object"},
    "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
    "context_id": 123,
    "date": date(2021, 3, 12),
    "place": "Carl's room",
    "place_id": 12,
    "country": "Netherlands",
    "region": "North Holland",
    "city": "Amsterdam",
    "objects": [{'type': 'chair', 'confidence': 0.68, 'id': 1},
                {'type': 'table', 'confidence': 0.79, 'id': 1}],
    "people": [{'name': 'Carl', 'confidence': 0.94, 'id': 1}]
}

```

Please ensure that the capsules to feed into the ``LongTermMemory`` object are well formed. When a field is not known
you may use an empty string (``""``) or ``None``.

### Logs

Please that note that initializing the ``LongTermMemory`` object requires a directory where to save the logging
information. By default the example scripts will use a temporary directory to store the logs, which will be cleaned
up after running the script. If you want to retain the logs you can specify a log folder with the `--logs` parameter
in each example script, e.g.

```shell
> python carl.py --logs my_log_dir
```

Every time a ``LongTermMemory`` object is initialized, a folder in the logs directory is created using the the current
timestamp. Every time information comes into the brain (e.g. every time a capsule is processed) a new ``.trig`` file is
created with a snapshot of the RDF triples created from the processing. 