import pathlib

import requests
from fuzzywuzzy import process

from cltl.brain.basic_brain import BasicBrain
from cltl.brain.utils.helper_functions import read_query, remove_articles
from cltl.combot.backend.utils.casefolding import casefold_text


class TypeReasoner(BasicBrain):

    def __init__(self, address, log_dir, clear_all=False):
        # type: (str, pathlib.Path, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        super(TypeReasoner, self).__init__(address, log_dir, clear_all, is_submodule=True)

    def reason_entity_type(self, item, exact_only=True):
        """
        Main function to determine if this item can be recognized by the brain, learned, or none
        Parameters
        ----------
        item: str
        exact_only: bool

        Returns
        -------

        """
        # Default
        learned_type = None
        text = ' I am sorry, I could not learn anything on %s so I will not remember it' % item

        # Clean label
        item_label = casefold_text(item, format='triple')
        item = remove_articles(item)

        # Item is in the ontology already as a class
        if item_label in self.get_classes():
            learned_type = item
            text = ' I know about %s. I will remember this object' % item

        # Item is in the ontology already as a label, return the type
        if not learned_type:
            mapping = self.get_labels_and_classes()
            if item_label in list(mapping.keys()):
                learned_type = mapping[item_label]
                text = f' I know about {item}. It is of type {learned_type}. I will remember this object'

        # Go at wikidata exact match
        if not learned_type:
            learned_type, description = self._exact_match_wikidata(item)
            if learned_type:
                text = f' I did not know what {item} is,' \
                       f' but I searched on Wikidata and I found that it is a {learned_type}.' \
                       f' I will remember this object'

        # Go at dbpedia exact match
        if not learned_type:
            learned_type, description = self._exact_match_dbpedia(item)
            if learned_type:
                text = f' I did not know what {item} is,' \
                       f' but I searched on Dbpedia and I found that it is a {learned_type}.' \
                       f' I will remember this object'

        # Second go at dbpedia, relaxed approach
        if not learned_type and not exact_only:
            learned_type, description = self._keyword_match_dbpedia(item)
            if learned_type:
                text = f' I did not know what {item} is,' \
                       f' but I searched for fuzzy matches on the web and I found that it is a {learned_type}.' \
                       f' I will remember this object'

        self._log.info(f"Reasoned type of {item} to: {learned_type}")

        return casefold_text(learned_type, format='triple'), text

    def _exact_match_dbpedia(self, item):
        """
        Query dbpedia for information on this item to get it's semantic type and description.
        :param item:
        :return:
        """
        url = 'http://dbpedia.org/sparql'

        # Gather combinations
        combinations = [item, item.capitalize(), item.lower(), item.title()]

        for comb in combinations:
            # Try exact matching query
            query = read_query('typing/dbpedia_type_and_description') % (comb, comb)

            try:
                r = requests.get(url, params={'format': 'json', 'query': query}, timeout=3)
                data = r.json() if r.status_code != 500 else None
            except Exception as e:
                self._log.warning("Failed to query DBpedia: %s", e)
                data = None

            # break if we have a hit
            if data and data['results']['bindings']:
                class_type = data['results']['bindings'][0]['label_type']['value'] \
                    if 'label_type' in list(data['results']['bindings'][0].keys()) else None
                description = data['results']['bindings'][0]['description']['value'] \
                    if 'description' in list(data['results']['bindings'][0].keys()) else None

                return class_type, description

        return None, None

    @staticmethod
    def _keyword_match_dbpedia(item):
        """
        Query Dbpedia using keyword search
        :param item:
        :return:
        """
        url = 'http://lookup.dbpedia.org/api/search.asmx/KeywordSearch'

        # Query API
        r = requests.get(url, params={'QueryString': item, 'MaxHits': '10'},
                         headers={'Accept': 'application/json'}).json()['results']

        # Fuzzy match
        choices = [e['label'] for e in r]
        best_match = process.extractOne("item", choices)

        # Get best match object
        r = [{'label': e['label'], 'classes': e['classes'], 'description': e['description']} for e in r if
             e['label'] == best_match[0]]

        if r:
            r = r[0]

            if r['classes']:
                # process dbpedia classes only
                r['classes'] = [c['label'] for c in r['classes'] if 'dbpedia' in c['uri']]

        else:
            r = {'label': None, 'classes': None, 'description': None}

        return r['classes'][0] if r['classes'] else None, r['description'].split('.')[0] if r['description'] else None

    def _exact_match_wikidata(self, item):
        """
        Query wikidata for information on this item to get it's semantic type and description.
        :param item:
        :return:
        """
        url = 'https://query.wikidata.org/sparql'

        # Gather combinations
        combinations = [item.lower()]

        for comb in combinations:
            # Try exact matching query
            query = read_query('typing/wikidata_type_and_description') % comb
            try:
                r = requests.get(url, params={'format': 'json', 'query': query}, timeout=3)
                data = r.json() if r.status_code == 200 else None
            except Exception as e:
                self._log.warning("Failed to query Wikidata: %s", e)
                data = None

            # break if we have a hit
            if data and data['results']['bindings']:
                class_type = data['results']['bindings'][0]['itemtypeLabel']['value'] \
                    if 'itemtypeLabel' in list(data['results']['bindings'][0].keys()) else None
                description = data['results']['bindings'][0]['itemDescription']['value'] \
                    if 'itemDescription' in list(data['results']['bindings'][0].keys()) else None

                return class_type, description

        return None, None
