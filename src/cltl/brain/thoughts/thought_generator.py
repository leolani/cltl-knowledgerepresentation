import pathlib
import random

from cltl.brain.basic_brain import BasicBrain
from cltl.brain.thoughts.completeness import Gaps, Gap
from cltl.brain.thoughts.correctness import CardinalityConflict, NegationConflict
from cltl.brain.thoughts.novelty import StatementNovelty, EntityNovelty
from cltl.brain.thoughts.overlap import Overlaps, Overlap
from cltl.brain.utils.helper_functions import read_query


class ThoughtGenerator(BasicBrain):

    def __init__(self, address, log_dir, clear_all=False):
        # type: (str, pathlib.Path, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        super(ThoughtGenerator, self).__init__(address, log_dir, clear_all, is_submodule=True)

    ########## novelty ##########
    def _fill_statement_novelty_(self, raw_provenance):
        """
        Structure statement novelty to get provenance if this statement has been heard before
        Parameters
        ----------
        raw_provenance: dict
            standard row result from SPARQL

        Returns
        -------
            StatementNovelty object containing provenance
        """
        preprocessed_date = self._rdf_builder.label_from_uri(raw_provenance['date']['value'], 'LC')
        processed_provenance = self._rdf_builder.fill_provenance(raw_provenance['authorlabel']['value'],
                                                                 preprocessed_date)

        return StatementNovelty(processed_provenance)

    def fill_entity_novelty(self, subject, complement):
        """
        Structure entity novelty to signal if these entities have been heard before
        Parameters
        ----------
        subject: Entity
            Instance as subject in the triple
        complement: Entity
            Instance as object in the triple

        Returns
        -------
            Entity object containing boolean values signaling if they are new
        """
        subject_novelty = self._check_instance_novelty_(subject.id)
        complement_novelty = self._check_instance_novelty_(complement.id)

        entity_novelty = EntityNovelty({"value": not subject_novelty, "entity": subject},
                                       {"value": not complement_novelty, "entity": complement})

        if entity_novelty.subject_novelty or entity_novelty.complement_novelty:
            self._log.info(f"Entity Novelty: {entity_novelty.__str__()} ")

        return entity_novelty

    def get_statement_novelty(self, statement_uri):
        """
        Query and build provenance if an instance (statement) has been learned before
        Parameters
        ----------
        statement_uri: str
            URI of instance

        Returns
        -------
        novelties: List[StatementNovelty]
            List of provenance for the instance
        """
        query = read_query('thoughts/statement_novelty') % statement_uri
        response = self._submit_query(query)

        if response and response[0] != {}:
            novelties = [self._fill_statement_novelty_(elem) for elem in response]
        else:
            novelties = []

        if novelties:
            n = random.choice(novelties)
            self._log.info(f"Statement Novelty: mentioned {len(response)} times, e.g. {n.__str__()}")

        return novelties

    def _check_instance_novelty_(self, instance_url):
        """
        Query if an instance (entity) has been heard about before
        Parameters
        ----------
        instance_url: str
            URI of instance

        Returns
        -------
        response: List[StatementNovelty]
            List of provenance for the instance
        """
        query = read_query('thoughts/entity_novelty') % instance_url
        response = self._submit_query(query, ask=True)

        return response

    ########## gaps ##########
    def _fill_entity_gap_(self, entity, raw_response):
        """
        Structure entity gap to get the predicate and range of what has been learned but not heard
        Parameters
        ----------
        entity: Entity
            entity for which we are getting gaps
        raw_response: dict
            standard row result from SPARQL

        Returns
        -------
            Gap object containing a predicate and its range/domain
        """

        processed_predicate = self._rdf_builder.fill_predicate(raw_response['p']['value'].split('/')[-1],
                                                               uri=raw_response['p']['value'])
        processed_range = self._rdf_builder.fill_entity('', namespace='N2MU',
                                                        types=[raw_response['type2']['value'].split('/')[-1]])

        return Gap(entity, processed_predicate, processed_range)

    def get_entity_gaps(self, entity, exclude=None):
        """
        Query and build gaps with regard to the range and domain of the given entity and its predicates
        Parameters
        ----------
        entity: Entity
            Entity for which we might get extra information
        exclude: Entity

        Returns
        -------
            Gaps object containing gaps related to range and domain information that could be learned
        """
        # Role as subject
        query = read_query('thoughts/subject_gaps') % (entity.id, entity.id if exclude is None else exclude.id)
        response = self._submit_query(query)

        if response:
            subject_gaps = [self._fill_entity_gap_(entity, elem)
                            for elem in response
                            if elem['p']['value'].split('/')[-1] not in self._NOT_TO_ASK_PREDICATES]

        else:
            subject_gaps = []

        # Role as object
        query = read_query('thoughts/object_gaps') % (entity.id, entity.id if exclude is None else exclude.id)
        response = self._submit_query(query)

        if response:
            complement_gaps = [self._fill_entity_gap_(entity, elem)
                               for elem in response
                               if elem['p']['value'].split('/')[-1] not in self._NOT_TO_ASK_PREDICATES]

        else:
            complement_gaps = []

        gaps = Gaps(subject_gaps, complement_gaps)

        if len(subject_gaps) > 0 or len(complement_gaps) > 0:
            self._log.info(f"Gaps: {gaps.__str__()}")

        return gaps

    ########## overlaps ##########
    def _fill_overlap_(self, raw_response):
        """
        Structure overlap to get the provenance and entity on which they overlap
        Parameters
        ----------
        raw_response: dict
            standard row result from SPARQL

        Returns
        -------
            Overlap object containing an entity and the provenance of the mention causing the overlap
        """
        preprocessed_date = self._rdf_builder.label_from_uri(raw_response['date']['value'], 'LC')
        preprocessed_types = self._rdf_builder.clean_aggregated_types(raw_response['types']['value'])

        processed_provenance = self._rdf_builder.fill_provenance(raw_response['authorlabel']['value'],
                                                                 preprocessed_date)
        processed_entity = self._rdf_builder.fill_entity(raw_response['label']['value'], preprocessed_types, 'LW')

        return Overlap(processed_provenance, processed_entity)

    def get_overlaps(self, capsule):
        """
        Query and build overlaps with regards to the subject and object of the heard statement
        Parameters
        ----------
        capsule: dict

        Returns
        -------
            Overlaps containing shared information with the heard statement
        """
        # Role as subject
        query = read_query('thoughts/object_overlap') % (capsule['triple'].predicate.id,
                                                         capsule['triple'].complement.id,
                                                         capsule['triple'].subject.id)
        response = self._submit_query(query)

        if response and response[0]['types']['value'] != '':
            complement_overlap = [self._fill_overlap_(elem) for elem in response]
        else:
            complement_overlap = []

        # Role as object
        query = read_query('thoughts/subject_overlap') % (capsule['triple'].predicate.id,
                                                          capsule['triple'].subject.id,
                                                          capsule['triple'].complement.id)
        response = self._submit_query(query)

        if response and response[0]['types']['value'] != '':
            subject_overlap = [self._fill_overlap_(elem) for elem in response]
        else:
            subject_overlap = []

        overlaps = Overlaps(subject_overlap, complement_overlap)

        if len(subject_overlap) > 0 or len(complement_overlap) > 0:
            self._log.info(f"Overlaps: {overlaps.__str__()}")

        return overlaps

    ########## conflicts ##########
    def _fill_cardinality_conflict_(self, raw_conflict):
        """
        Structure cardinality conflict to pair provenance and object that creates the conflict
        Parameters
        ----------
        raw_conflict: dict
            standard row result from SPARQL

        Returns
        -------
            CardinalityConflict object containing provenance and entity
        """
        processed_provenance = self._rdf_builder.fill_provenance(raw_conflict['authorlabel']['value'],
                                                                 raw_conflict['date']['value'])
        processed_type = self.get_type_of_instance(raw_conflict['o']['value'])
        processed_entity = self._rdf_builder.fill_entity(raw_conflict['objectLabel']['value'], processed_type)

        return CardinalityConflict(processed_provenance, processed_entity)

    def _fill_negation_conflict_(self, raw_conflict):
        """
        Structure negation conflict to pair provenance and predicate that creates the conflict
        Parameters
        ----------
        raw_conflict: dict
            standard row result from SPARQL

        Returns
        -------
            NegationConflict object containing provenance and predicate
        """
        preprocessed_date = self._rdf_builder.label_from_uri(raw_conflict['date']['value'], 'LC')
        processed_provenance = self._rdf_builder.fill_provenance(raw_conflict['authorlabel']['value'],
                                                                 preprocessed_date)
        processed_polarity = self._rdf_builder.label_from_uri(raw_conflict['val']['value'], 'GRASPf')

        return NegationConflict(processed_provenance, processed_polarity)

    def get_all_conflicts(self):
        """
        Aggregate all conflicts in brain
        :return:
        """
        conflicts = []
        for predicate in self._ONE_TO_ONE_PREDICATES:
            conflicts.extend(self.get_conflicts_with_one_to_one_predicate(predicate))

        return conflicts

    def get_conflicts_with_one_to_one_predicate(self, one_to_one_predicate):
        query = read_query('one_to_one_conflicts') % one_to_one_predicate

        response = self._submit_query(query)
        conflicts = []
        for item in response:
            conflict = {'subject': item['sname']['value'], 'predicate': one_to_one_predicate, 'objects': []}

            for x in item['pairs']['value'].split(';'):
                [val, auth] = x.split(',')
                option = {'value': val, 'author': auth}
                conflict['objects'].append(option)

            conflicts.append(conflict)

        return conflicts

    def get_complement_cardinality_conflicts(self, capsule):
        """
        Query and build cardinality conflicts, meaning conflicts because predicates should be one to one but have
        multiple object values
        Parameters
        ----------
        capsule: dict

        Returns
        -------
        conflicts: List[CardinalityConflict]
            List of Conflicts containing the object which creates the conflict, and their provenance
        """
        if str(capsule['triple'].predicate_name) not in self._ONE_TO_ONE_PREDICATES:
            return []

        query = read_query('thoughts/object_cardinality_conflicts') % (capsule['triple'].predicate.id,
                                                                       capsule['triple'].subject.id,
                                                                       capsule['triple'].complement.id)

        response = self._submit_query(query)
        if response and response[0] != {}:
            conflicts = [self._fill_cardinality_conflict_(elem) for elem in response]
        else:
            conflicts = []

        if conflicts:
            c = random.choice(conflicts)
            self._log.info(f"Cardinality Conflict: {c.__str__()}")

        return conflicts

    def get_negation_conflicts(self, capsule):
        """
        Query and build negation conflicts, meaning conflicts because predicates are directly negated
        Parameters
        ----------
        capsule: dict

        Returns
        -------
        conflicts: List[NegationConflict]
            List of Conflicts containing the predicate which creates the conflict, and their provenance
        """
        conflicts = []

        query = read_query('thoughts/negation_conflicts') % (capsule['triple'].predicate.id,
                                                             capsule['triple'].subject.id,
                                                             capsule['triple'].complement.id)

        response = self._submit_query(query)
        if response and response[0] != {} and len(response) > 2:
            affirmative_conflict = [item for item in response if item['val']['value'].split('#')[-1] == 'POSITIVE']
            negative_conflict = [item for item in response if item['val']['value'].split('#')[-1] == 'NEGATIVE']

            if affirmative_conflict or negative_conflict:
                conflicts = [self._fill_negation_conflict_(elem) for elem in response]

        if conflicts:
            c = random.choice(conflicts)
            self._log.info(f"Negation Conflicts: {c.__str__()}")

        return conflicts
