import pathlib

from cltl.brain.LTM_question_processing import create_query
from cltl.brain.LTM_statement_processing import model_graphs, _link_leolani, _link_entity, \
    create_claim_graph
from cltl.brain.basic_brain import BasicBrain
from cltl.brain.infrastructure import Thoughts, Triple
from cltl.brain.reasoners import LocationReasoner, ThoughtGenerator, TypeReasoner, TrustCalculator
from cltl.brain.utils.helper_functions import read_query
from cltl.combot.backend.api.discrete import UtteranceType
from cltl.combot.backend.utils.casefolding import casefold_text

from datetime import datetime


class LongTermMemory(BasicBrain):
    def __init__(self, address, log_dir, clear_all=False):
        # type: (str, pathlib.Path, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        super(LongTermMemory, self).__init__(address, log_dir, clear_all)

        self.myself = None
        self.query_prefixes = read_query('prefixes')  # USED ONLY WHEN QUERYING
        self.thought_generator = ThoughtGenerator(address, log_dir)
        self.location_reasoner = LocationReasoner(address, log_dir)
        self.type_reasoner = TypeReasoner(address, log_dir)
        self.trust_calculator = TrustCalculator(address, log_dir)

        self.set_location_label = self.location_reasoner.set_location_label
        self.reason_location = self.location_reasoner.reason_location

        self.trust_calculator.compute_trust_network()

    #################################### Main functions to interact with the brain ####################################
    def get_thoughts_on_entity(self, entity_label, reason_types=False):
        if entity_label is not None and entity_label != '':

            # Try to figure out what this entity is
            entity_type = None
            if reason_types:
                entity_type, _ = self.type_reasoner.reason_entity_type(entity_label, exact_only=True)

            # Casefold
            entity_label = casefold_text(entity_label, format='triple')

            # Create entity
            if entity_type is not None:
                entity_types = [casefold_text(entity_type, format='triple'), 'Instance', 'object']
            else:
                entity_types = [casefold_text(entity_label, format='triple'), 'Instance', 'object']

            entity = self._rdf_builder.fill_entity(entity_label, entity_types, 'LW')

            # Create graphs and triples
            _link_leolani(self)
            predicate = self._rdf_builder.fill_predicate('see')
            _link_entity(self, entity, self.instance_graph, create_label=True)
            create_claim_graph(self, self.myself, predicate, entity)
            triple = Triple(self.myself, predicate, entity)

            # Check how many items of the same type as subject and complement we have
            entity_novelty = self.thought_generator.fill_entity_novelty(self.myself.id, entity.id)

            # Finish process of uploading new knowledge to the triple store
            data = self._serialize(self._brain_log())
            code = self._upload_to_brain(data)

            # Check for gaps, in case we want to be proactive
            entity_gaps = self.thought_generator.get_entity_gaps(entity)

            # Create JSON output
            thoughts = Thoughts([], entity_novelty, [], [], None, entity_gaps, None, None)
            output = {'response': code, 'triple': triple, 'thoughts': thoughts}

        else:
            # Create JSON output
            output = {'response': None, 'triple': None, 'thoughts': None}

        return output

    def update(self, capsule, reason_types=False, create_label=False):
        # type (Utterance) -> Thoughts
        """
        Main function to interact with if a statement is coming into the brain. Takes in an Utterance containing a
        parsed statement as a Triple, transforms them to linked data, and posts them to the triple store
        Parameters
        ----------
        capsule: dict
            Contains all necessary information regarding a statement just made.
        reason_types: Boolean
            Signal to entity linking over the semantic web
        create_label: Boolean
            Turn automatic rdfs:label on or off for instance graph entities

        Returns
        -------
        capsule: dict
            Returns back the capsule, adding the response code and thoughts, which contains information about conflicts,
            novelty, gaps and overlaps that the statement produces given the data in the triple store

        """

        # Process capsule to right types
        capsule['triple'] = self._rdf_builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])
        capsule['perspective'] = self._rdf_builder.fill_perspective(capsule['perspective']) \
            if 'perspective' in capsule.keys() else self._rdf_builder.fill_perspective({})
        capsule['utterance_type'] = UtteranceType[capsule['utterance_type']] \
            if type(capsule['utterance_type']) == str else capsule['utterance_type']
        capsule['date'] = datetime.fromisoformat(capsule['date']).date() \
            if type(capsule['date']) == str else capsule['date']

        if capsule['triple'] is not None:

            # Try to figure out what this entity is
            if reason_types:
                if not capsule['triple'].complement.types:
                    complement_type, _ = self.type_reasoner.reason_entity_type(str(capsule['triple'].complement_name),
                                                                               exact_only=True)
                    capsule['triple'].complement.add_types([complement_type])

                if not capsule['triple'].subject.types:
                    subject_type, _ = self.type_reasoner.reason_entity_type(str(capsule['triple'].subject_name),
                                                                            exact_only=True)
                    capsule['triple'].complement.add_types([subject_type])

            # Casefold
            capsule['triple'].casefold(format='triple')
            capsule['author'] = casefold_text(capsule['author'], format='triple')

            # Create graphs and triples
            instance = model_graphs(self, capsule, create_label)

            # Check if this knowledge already exists on the brain
            statement_novelty = self.thought_generator.get_statement_novelty(instance.id)

            # Check how many items of the same type as subject and complement we have
            entity_novelty = self.thought_generator.fill_entity_novelty(capsule['triple'].subject.id,
                                                                        capsule['triple'].complement.id)

            # Find any overlaps
            overlaps = self.thought_generator.get_overlaps(capsule)

            # Finish process of uploading new knowledge to the triple store
            data = self._serialize(self._brain_log())
            code = self._upload_to_brain(data)

            # Check for conflicts after adding the knowledge
            negation_conflicts = self.thought_generator.get_negation_conflicts(capsule)
            cardinality_conflict = self.thought_generator.get_complement_cardinality_conflicts(capsule)

            # Check for gaps, in case we want to be proactive
            subject_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].subject,
                                                                  exclude=capsule['triple'].complement)
            complement_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].complement,
                                                                     exclude=capsule['triple'].subject)

            # Report trust
            actor = self._rdf_builder.fill_entity(capsule['author'], ['Instance', 'Source', 'Actor', 'person'], 'LF')
            trust = self.trust_calculator.get_trust(actor.id)

            # Create JSON output
            thoughts = Thoughts(statement_novelty, entity_novelty, negation_conflicts, cardinality_conflict,
                                subject_gaps, complement_gaps, overlaps, trust)
            output = {'response': code, 'statement': capsule, 'thoughts': thoughts}

        else:
            # Create JSON output
            output = {'response': None, 'statement': capsule, 'thoughts': None}

        return output

    def experience(self, utterance, create_label=False):
        """
        Main function to interact with if an experience is coming into the brain. Takes in a structured utterance
        containing parsed experience, transforms them to triples, and posts them to the triple store
        :param utterance: dict
        :param create_label: Boolean
            Turn automatic rdfs:label on or off for instance graph entities
        :return: json response containing the status for posting the triples, and the original statement
        """
        # Create graphs and triples
        _ = model_graphs(self, utterance, create_label)

        # Finish process of uploading new knowledge to the triple store
        data = self._serialize(self._brain_log())
        code = self._upload_to_brain(data)

        # Create JSON output
        output = {'response': code, 'statement': utterance}

        return output

    def query_brain(self, capsule):
        """
        Main function to interact with if a question is coming into the brain. Takes in a structured parsed question,
        transforms it into a query, and queries the triple store for a response
        :param capsule: Structured data of a parsed question
        :return: json response containing the results of the query, and the original question
        """
        capsule['triple'] = self._rdf_builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])

        # Generate query
        query = create_query(self, capsule)
        # Perform query
        response = self._submit_query(query)

        # Create JSON output
        output = {'response': response, 'question': capsule}

        return output
