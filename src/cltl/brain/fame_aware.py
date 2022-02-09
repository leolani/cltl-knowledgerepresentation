import pathlib

import requests

from cltl.brain.LTM_statement_processing import _link_entity, create_claim_graph
from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import read_query
from cltl.combot.backend.utils.casefolding import casefold_text


class FameAwareMemory(LongTermMemory):
    def __init__(self, address, log_dir, clear_all=False):
        # type: (str, pathlib.Path, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        super(FameAwareMemory, self).__init__(address, log_dir, clear_all)

    def lookup_person_wikidata(self, person_name):
        """
        Query wikidata for information on this item to get it's semantic type and description.
        :param person_name:
        :return: output: Dictionary with the response of the process. 200 signals knowledge was acquired
        """
        url = 'https://query.wikidata.org/sparql'

        # Gather combinations
        combinations = [person_name, person_name.capitalize(), person_name.lower(), person_name.title()]

        for comb in combinations:
            # Try exact matching query
            query = read_query('famous_person') % (comb, comb, comb)
            try:
                r = requests.get(url, params={'format': 'json', 'query': query}, timeout=3)
                data = r.json() if r.status_code == 200 else None
            except:
                self._log.exception("Failed to query Wikidata")
                data = None

            # break if we have a hit
            if data and data['results']['bindings']:
                # Report on size of graph found
                total_triples = len(data['results']['bindings'])
                self._log.info(f"{total_triples} triples found for {comb}")

                for triple in data['results']['bindings']:
                    # Add claim to the dataset
                    self.add_triple(triple)

                # Finish process of uploading new knowledge to the triple store
                data = self._serialize(self._brain_log())
                code = self._upload_to_brain(data)

                return {'response': code, 'label': person_name, 'data': data}

        return {'response': None, 'label': person_name, 'data': None}

    def add_triple(self, triple):

        # Parse subject
        s_types = self._rdf_builder.clean_aggregated_types(triple['subjectTypesLabel']['value'])
        s = self._rdf_builder.fill_entity(casefold_text(triple['subjectLabel']['value'], format='triple'),
                                          s_types, uri=triple['subject']['value'])
        _link_entity(self, s, self.instance_graph, create_label=True)

        # Parse predicate
        p = self._rdf_builder.fill_predicate(casefold_text(triple['propLabel']['value'], format='triple'),
                                             uri=triple['property']['value'])

        # Parse object
        if 'literal' in triple['objectTypesLabel']['value']:
            o = self._rdf_builder.fill_literal(casefold_text(triple['objectLabel']['value'], format='triple'))
            self.instance_graph.add((s.id, p.id, o))
        else:
            o_types = self._rdf_builder.clean_aggregated_types(triple['objectTypesLabel']['value'])
            o = self._rdf_builder.fill_entity(casefold_text(triple['objectLabel']['value'], format='triple'),
                                              o_types, uri=triple['object']['value'])
            _link_entity(self, o, self.instance_graph, create_label=True)
            create_claim_graph(self, s, p, o)

        # self._log.info(f'Triple: {}')
