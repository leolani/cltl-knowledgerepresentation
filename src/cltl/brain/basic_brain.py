import json
import pathlib
from datetime import datetime

from cltl.brain import logger
from cltl.brain.infrastructure import StoreConnector, RdfBuilder
from cltl.brain.utils.helper_functions import read_query


class BasicBrain(object):
    _ONE_TO_ONE_PREDICATES = [
        'be-from',
        'born_in',
        'favorite',
        'live-in',
        'work-at'
    ]

    _NOT_TO_ASK_PREDICATES = ['faceID', 'name']

    def __init__(self, address, log_dir, clear_all=False, is_submodule=False):
        # type: (str, pathlib.Path, bool, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """
        self._connection = StoreConnector(address, format='trig')
        self._rdf_builder = RdfBuilder()

        self._log = logger.getChild(self.__class__.__name__)
        self._log.info("Booted")

        self.log_dir = log_dir.joinpath(f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}")
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Start with a clean local memory
        self.assign_local_memory()

        if not is_submodule:
            # Possible clear all contents (testing purposes)
            if clear_all:
                self.clear_brain()

            # Upload ontology here
            self.upload_ontology()

    ########## basic post get behaviour ##########
    def _upload_to_brain(self, data):
        """
        Post data to the brain
        :param data: serialized data as string
        :return: response status
        """
        self._log.debug("Posting triples")

        return self._connection.upload(data)

    def _submit_query(self, query, ask=False, post=False):
        """
        Submit a query to the triple store
        Parameters
        ----------
        query: str
            SPARQL query to be posted
        ask: bool
            Whether the query is of type ask, in which case the structure of the response changes

        Returns
        -------

        """
        self._log.debug("Posting query")

        return self._connection.query(query, ask=ask, post=post)

    def _brain_log(self):
        return self.log_dir.joinpath(f"brain_log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")

    ########## brain structure exploration ##########
    def _serialize(self, file_path):
        """
        Save graph to local file and return the serialized string
        :param file_path: path to where data will be saved
        :return: serialized data as string
        """
        # Save to file and return the string representation
        with open(f'{file_path}.{self._connection.format}', 'wb') as f:
            self.dataset.serialize(f, format=self._connection.format)

        data = self.dataset.serialize(format=self._connection.format)

        # Clear local memory
        # TODO fix bug
        # self._rdf_builder.fresh_local_memory()
        self.assign_local_memory()

        return data

    def upload_ontology(self):
        """
        Upload ontology
        :return: response status
        """
        if not self.ontology_is_uploaded():
            self._rdf_builder.load_ontologies()

            self._log.info("Uploading ontology to brain")
            data = self._serialize(self._brain_log())
            self._connection.upload(data)

    def ontology_is_uploaded(self):
        """
        Query the existence of the Ontology graph, thus not importing the whole Ontology every time
        :return: response status
        """
        self._log.debug("Checking if ontology is in brain")
        query = read_query('structure exploration/ontology_uploaded')
        response = self._submit_query(query, ask=True)

        return response

    def get_predicates(self):
        """
        Get predicates in social ontology
        :return:
        """
        query = read_query('structure exploration/predicates')
        response = self._submit_query(query)

        return [elem['p']['value'].split('/')[-1] for elem in response]

    def get_classes(self):
        """
        Get classes or types in social ontology
        :return:
        """
        query = read_query('structure exploration/classes')
        response = self._submit_query(query)

        return [elem['c']['value'].split('/')[-1] for elem in response]

    def get_labels_and_classes(self):
        """
        Get classes in social ontology
        :return:
        """
        query = read_query('structure exploration/labels_and_classes')
        response = self._submit_query(query)

        temp = dict()
        for r in response:
            temp[r['l']['value']] = r['type']['value'].split('/')[-1]

        return temp

    def get_ontology_elements(self):
        """
        Get classes, object and data properties in ontology
        :return:
        """
        query = read_query('structure exploration/ontology_elements')
        response = self._submit_query(query)

        temp = dict()
        for r in response:
            temp[r['name']['value']] = r['prefixedName']['value']

        return temp

    def get_jsonld_context(self, save_path=False):
        """
        Create context for json ld interpretation
        :param save_path: file path to save JSON, if false then JSON is only returned as string
        :return: str
        """
        # Create JSON LD
        namespaces = dict()
        for k, v in self.namespaces.items():
            namespaces[k.lower()] = str(v)

        ontology = self.get_ontology_elements()

        my_jsonld = {**namespaces, **ontology}

        if save_path:
            with open(save_path, 'w') as f:
                json.dump(my_jsonld, f, indent=4)

        final = json.dumps(my_jsonld, indent=4)

        return final

    ########## learned facts exploration ##########
    def count_triples(self):
        """
        Count triples in the brain
        :return:
        """
        query = read_query('content exploration/count_triples')
        response = self._submit_query(query)
        return float(response[0]['triples']['value'])

    def count_statements(self):
        """
        Count statements or 'facts' in the brain
        :return:
        """
        query = read_query('content exploration/count_statements')
        response = self._submit_query(query)
        return float(response[0]['count']['value'])

    def count_statements_by(self, actor_uri):
        """
        Count statements or 'facts' in the brain by a given author
        :return:
        """
        query = read_query('trust/count_statements_by') % actor_uri
        response = self._submit_query(query)
        return float(response[0]['num_stat']['value'])

    def novel_statements_by(self, actor_uri):
        """
        Return statements or 'facts' in the brain by a given author, that have not been heard from anyone else
        :return:
        """
        query = read_query('trust/novel_statements_by') % actor_uri
        response = self._submit_query(query)
        return [elem['statement']['value'].split('/')[-1] for elem in response]

    def count_perspectives(self):
        """
        Count perspectives or 'views' in the brain
        :return:
        """
        query = read_query('content exploration/count_perspectives')
        response = self._submit_query(query)
        return float(response[0]['count']['value'])

    def get_all_negation_conflicts(self):
        """
        Count conflicts or 'facts' with opposing polarity in the brain
        :return:
        """
        query = read_query('content exploration/all_negation_conflicts')
        response = self._submit_query(query)
        return response

    def get_conflicts_by(self, actor_uri):
        """
        Return conflicts or 'facts' with opposing polarity in the brain stated by a specific actor
        :return:
        """
        # TODO: fix query to work on subproperties
        query = read_query('trust/conflicts_by') % (actor_uri, actor_uri)
        response = self._submit_query(query)
        return response

    def count_friends(self):
        """
        Count number of people I have talked to
        :return:
        """
        query = read_query('content exploration/count_friends')
        response = self._submit_query(query)
        return float(response[0]['count']['value'])

    def get_my_friends(self):
        """
        Get names of people I have talked to
        :return:
        """
        query = read_query('content exploration/my_friends')
        response = self._submit_query(query)
        return [elem['friend']['value'].split('/')[-1] for elem in response]

    def get_best_friends(self):
        """
        Get names of the 5 people I have talked to the most
        :return:
        """
        query = read_query('content exploration/best_friends')
        response = self._submit_query(query)
        return [(elem['act']['value'], elem['num_chat']['value'].split('/')[-1]) for elem in response]

    def when_last_chat_with(self, actor_uri):
        """
        Get time value for the last time I chatted with this person
        :param actor_uri: uri of person
        :return:
        """
        query = read_query('trust/when_last_chat_with') % actor_uri
        response = self._submit_query(query)

        return response[0]['time']['value'].split('/')[-1] if response != [] else ''

    def count_chat_with(self, actor_uri):
        """
        Count times I chatted with this person
        :param actor_uri: uri of person
        :return:
        """
        query = read_query('trust/count_chat_with') % actor_uri
        response = self._submit_query(query)

        return float(response[0]['num_chats']['value'].split('/')[-1]) if response != [] else 0.0

    def count_instances(self):
        """
        Count instances or world entities in the brain
        :return:
        """
        query = read_query('content exploration/count_instances')
        response = self._submit_query(query)
        return float(response[0]['count']['value'])

    def get_instance_of_type(self, instance_type):
        """
        Get instances of a certain class type
        :param instance_type: name of class in ontology
        :return:
        """
        query = read_query('typing/instance_of_type') % instance_type
        response = self._submit_query(query)
        return [elem['s']['value'] for elem in response] if response else []

    def get_type_of_instance(self, instance_uri):
        """
        Get types of a certain instance identified by its label
        :param instance_uri: uri of instance
        :return:
        """
        query = read_query('typing/type_of_instance') % instance_uri
        response = self._submit_query(query)
        return [elem['type']['value'] for elem in response] if response else []

    def get_id_of_instance(self, uri):
        """
        Get ids of a certain instance identified by its label
        :param uri: label of instance
        :return:
        """
        query = read_query('id/id_of_instance') % uri
        response = self._submit_query(query)
        return [elem['id']['value'] for elem in response] if response else []

    def get_triples_with_predicate(self, predicate_uri):
        """
        Get triples that contain this predicate
        :param predicate_uri:
        :return:
        """
        query = read_query('content exploration/triples_with_predicate') % predicate_uri
        response = self._submit_query(query)
        return [(elem['s']['value'], elem['o']['value']) for elem in response]

    ########## WARNING deletions area ##########

    def clear_brain(self):
        """
        Clear all data from the brain
        :return: response status
        """
        self._log.info("Clearing brain")
        query = "DROP ALL "
        _ = self._connection.query(query, post=True)

    def assign_local_memory(self):
        """
        Assign direct access to rdf builder attributes
        Returns
        -------

        """

        self.namespaces = self._rdf_builder.namespaces
        self.dataset = self._rdf_builder.dataset

        self.ontology_graph = self._rdf_builder.ontology_graph
        self.instance_graph = self._rdf_builder.instance_graph
        self.claim_graph = self._rdf_builder.claim_graph
        self.perspective_graph = self._rdf_builder.perspective_graph
        self.interaction_graph = self._rdf_builder.interaction_graph
