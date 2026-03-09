import pathlib
from datetime import datetime

from cltl.commons.casefolding import casefold_text
from cltl.commons.discrete import UtteranceType

from cltl.brain.LTM_context_processing import process_context
from cltl.brain.LTM_experience_processing import process_experience, process_visual_relation
from cltl.brain.LTM_mention_processing import process_mention
from cltl.brain.LTM_question_processing import create_query
from cltl.brain.LTM_shared import _create_actor
from cltl.brain.LTM_statement_processing import process_statement
from cltl.brain.basic_brain import BasicBrain
from cltl.brain.infrastructure import Thoughts
from cltl.brain.reasoners import LocationReasoner, ThoughtGenerator, TypeReasoner, TrustCalculator
from cltl.brain.utils.helper_functions import read_query


class LongTermMemory(BasicBrain):
    def __init__(self, address, log_dir, clear_all=False, calculate_trust=False):
        # type: (str, pathlib.Path, bool, bool) -> None
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

        # Initialize submodules
        self.thought_generator = ThoughtGenerator(address, log_dir)
        self.location_reasoner = LocationReasoner(address, log_dir)
        self.type_reasoner = TypeReasoner(address, log_dir)
        self.trust_calculator = TrustCalculator(address, log_dir)

        self.set_location_label = self.location_reasoner.set_location_label
        self.reason_location = self.location_reasoner.reason_location

        if calculate_trust:
            self.trust_calculator.compute_trust_network()

    #################################### Main functions to interact with the brain ####################################
    def query_brain(self, capsule):
        # type (dict) -> dict
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
        output = {'response': response, 'question': capsule, 'rdf_log_path': None}

        return output

    def capsule_context(self, capsule):
        # type (dict) -> dict
        """
        Main function to initialize an episode by creating a context with time and location details.
        Parameters
        ----------
        capsule: dict
            Contains all necessary information regarding a situated context (context_id, date, place name and id,
            country, region, and city).

        Returns
        -------
        capsule: dict
            Returns back the capsule, adding the response code.

        """

        # Process capsule to right types
        capsule['date'] = datetime.fromisoformat(capsule['date']).date() \
            if type(capsule['date']) == str else capsule['date']

        # Create graphs and triples
        context = process_context(self, capsule)

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        # Create JSON output
        output = {'response': code, 'context': capsule, 'rdf_log_path': rdf_log_path}

        return output

    def capsule_statement(self, capsule, reason_types=False, return_thoughts=True, create_label=False):
        # type (dict) -> dict
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
        # Try to figure out what this entity is
        if reason_types:
            if not capsule['subject']['type'] or capsule['subject']['type'] == '':
                subject_type, _ = self.type_reasoner.reason_entity_type(capsule['subject']['label'], exact_only=True)
                capsule['subject']['type'] = [subject_type]

            if not capsule['object']['type'] or capsule['object']['type'] == '':
                object_type, _ = self.type_reasoner.reason_entity_type(capsule['object']['label'], exact_only=True)
                capsule['object']['type'] = [object_type]

        # Process capsule to right types
        capsule['triple'] = self._rdf_builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])
        capsule['perspective'] = self._rdf_builder.fill_perspective(capsule['perspective']) \
            if 'perspective' in capsule.keys() else self._rdf_builder.fill_perspective({})
        capsule['utterance_type'] = UtteranceType[capsule['utterance_type']] \
            if type(capsule['utterance_type']) == str else capsule['utterance_type']

        # Casefold
        capsule['triple'].casefold(format='triple')
        capsule['author']['type'] = [casefold_text(t, format='triple') for t in capsule['author']['type']]

        # Create graphs and triples
        claim = process_statement(self, capsule, create_label)

        if return_thoughts:
            # Check if this knowledge already exists on the brain
            statement_novelty = self.thought_generator.get_statement_novelty(claim.id)

            # Check how many items of the same type as subject and complement we have
            entity_novelty = self.thought_generator.fill_entity_novelty(capsule['triple'].subject.id,
                                                                        capsule['triple'].complement.id)

            # Find any overlaps
            overlaps = self.thought_generator.get_overlaps(capsule)
        else:
            statement_novelty = None
            entity_novelty = None
            overlaps = None

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        if return_thoughts:
            # Check for conflicts after adding the knowledge
            negation_conflicts = self.thought_generator.get_negation_conflicts(capsule)
            cardinality_conflicts = self.thought_generator.get_complement_cardinality_conflicts(capsule)

            # Check for gaps, in case we want to be proactive
            subject_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].subject,
                                                                  exclude=capsule['triple'].complement)
            complement_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].complement,
                                                                     exclude=capsule['triple'].subject)

            # Report trust
            actor, _ = _create_actor(self, capsule, create_label)
            trust = self.trust_calculator.get_trust(actor.id)
        else:
            negation_conflicts = None
            cardinality_conflicts = None
            subject_gaps = None
            complement_gaps = None
            trust = None

        # Create JSON output
        thoughts = Thoughts(statement_novelty, entity_novelty, negation_conflicts, cardinality_conflicts,
                            subject_gaps, complement_gaps, overlaps, trust)
        output = {'response': code, 'statement': capsule, 'thoughts': thoughts, 'rdf_log_path': rdf_log_path}

        return output


    def capsule_event(self, capsule, reason_types=False, return_thoughts=True, create_label=False):
        # type (dict) -> dict
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
        # Try to figure out what this entity is
        if reason_types:
            for triple in capsule['event_details']:
                if not triple['subject']['type'] or triple['subject']['type'] == '':
                    subject_type, _ = self.type_reasoner.reason_entity_type(triple['subject']['label'], exact_only=True)
                    triple['subject']['type'] = [subject_type]

                if not triple['object']['type'] or triple['object']['type'] == '':
                    object_type, _ = self.type_reasoner.reason_entity_type(triple['object']['label'], exact_only=True)
                    triple['object']['type'] = [object_type]

        # # Process capsule to right types
        capsule['triple_list'] = []
        for item in capsule["event_details"]:
            triple = self._rdf_builder.fill_event_triple(item['subject'], item['predicate'], item['object'])
            capsule['triple_list'].append(triple)
        capsule['perspective'] = self._rdf_builder.fill_perspective(capsule['perspective']) \
             if 'perspective' in capsule.keys() else self._rdf_builder.fill_perspective({})
        capsule['utterance_type'] = UtteranceType[capsule['utterance_type']] \
             if type(capsule['utterance_type']) == str else capsule['utterance_type']
        #
        # # Casefold
        # capsule['triple'].casefold(format='triple')
        # capsule['author']['type'] = [casefold_text(t, format='triple') for t in capsule['author']['type']]

        # Create graphs and triples
        claim = process_statement(self, capsule, create_label)

        # We set return_thoughts to False, because the thought functions have not been adapted for triple_list and not for events as subject   '
        return_thoughts = False
        statement_novelty = []
        entity_novelty = False
        overlaps = []
        if return_thoughts:
            for triple in capsule['triple_list']:
                # Check if this knowledge already exists on the brain []
                triple_statement_novelty = self.thought_generator.get_statement_novelty(claim.id)
                statement_novelty.extend(triple_statement_novelty)
                # Check how many items of the same type as subject and complement we have
               # boolean_value
                triple_entity_novelty = self.thought_generator.fill_entity_novelty(triple.subject.id,  triple.complement.id)
                if entity_novelty is None:
                    entity_novelty = triple_entity_novelty
                # Find any overlaps []
                triple_overlaps = self.thought_generator.get_overlaps(triple)
                overlaps.extend(triple_overlaps)
        else:
            statement_novelty = None
            entity_novelty = None
            overlaps = None

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        negation_conflicts = []
        cardinality_conflicts = []
        subject_gaps = []
        complement_gaps = []

        if return_thoughts:
            for triple in capsule['triple_list']:
                # Check for conflicts after adding the knowledge
                triple_negation_conflicts = self.thought_generator.get_negation_conflicts(triple)
                negation_conflicts.extend(triple_negation_conflicts)

                triple_cardinality_conflicts = self.thought_generator.get_complement_cardinality_conflicts(triple)
                cardinality_conflicts.extend(triple_cardinality_conflicts)

                # Check for gaps, in case we want to be proactive
                triple_subject_gaps = self.thought_generator.get_entity_gaps(entity=triple.subject,
                                                                      exclude=triple.complement)
                subject_gaps.extend(triple_subject_gaps)

                triple_complement_gaps = self.thought_generator.get_entity_gaps(entity=triple.complement,
                                                                         exclude=triple.subject)
                complement_gaps.extends[triple_complement_gaps]
                # Report trust
                # actor, _ = _create_actor(self, capsule, create_label)
                # trust = self.trust_calculator.get_trust(actor.id)
        else:
            negation_conflicts = None
            cardinality_conflicts = None
            subject_gaps = None
            complement_gaps = None
            trust = None

        # Create JSON output
        thoughts = Thoughts(statement_novelty, entity_novelty, negation_conflicts, cardinality_conflicts,
                            subject_gaps, complement_gaps, overlaps, trust)
        output = {'response': code, 'statement': capsule, 'thoughts': thoughts, 'rdf_log_path': rdf_log_path}

        return output

    def capsule_experience_triple(self, capsule, reason_types=False, return_thoughts=True, create_label=False):
        # type (dict) -> dict
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
        # Try to figure out what this entity is
        if reason_types:
            if not capsule['subject']['type'] or capsule['subject']['type'] == '':
                subject_type, _ = self.type_reasoner.reason_entity_type(capsule['subject']['label'], exact_only=True)
                capsule['subject']['type'] = [subject_type]

            if not capsule['object']['type'] or capsule['object']['type'] == '':
                object_type, _ = self.type_reasoner.reason_entity_type(capsule['object']['label'], exact_only=True)
                capsule['object']['type'] = [object_type]

        # Process capsule to right types
        capsule['triple'] = self._rdf_builder.fill_triple(capsule['subject'], capsule['predicate'], capsule['object'])
        capsule['perspective'] = self._rdf_builder.fill_perspective(capsule['perspective']) \
            if 'perspective' in capsule.keys() else self._rdf_builder.fill_perspective({})
        capsule['utterance_type'] = UtteranceType[capsule['utterance_type']] \
            if type(capsule['utterance_type']) == str else capsule['utterance_type']

        # Casefold
        capsule['triple'].casefold(format='triple')
        capsule['source']['type'] = [casefold_text(t, format='triple') for t in capsule['source']['type']]

        # Create graphs and triples
        claim = process_statement(self, capsule, create_label)

        if return_thoughts:
            # Check if this knowledge already exists on the brain
            statement_novelty = self.thought_generator.get_statement_novelty(claim.id)

            # Check how many items of the same type as subject and complement we have
            entity_novelty = self.thought_generator.fill_entity_novelty(capsule['triple'].subject.id,
                                                                        capsule['triple'].complement.id)

            # Find any overlaps
            overlaps = self.thought_generator.get_overlaps(capsule)
        else:
            statement_novelty = None
            entity_novelty = None
            overlaps = None

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        if return_thoughts:
            # Check for conflicts after adding the knowledge
            negation_conflicts = self.thought_generator.get_negation_conflicts(capsule)
            cardinality_conflicts = self.thought_generator.get_complement_cardinality_conflicts(capsule)

            # Check for gaps, in case we want to be proactive
            subject_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].subject,
                                                                  exclude=capsule['triple'].complement)
            complement_gaps = self.thought_generator.get_entity_gaps(entity=capsule['triple'].complement,
                                                                     exclude=capsule['triple'].subject)

            # Report trust
            actor, _ = _create_actor(self, capsule, create_label)
            trust = self.trust_calculator.get_trust(actor.id)
        else:
            negation_conflicts = None
            cardinality_conflicts = None
            subject_gaps = None
            complement_gaps = None
            trust = None

        # Create JSON output
        thoughts = Thoughts(statement_novelty, entity_novelty, negation_conflicts, cardinality_conflicts,
                            subject_gaps, complement_gaps, overlaps, trust)
        output = {'response': code, 'statement': capsule, 'thoughts': thoughts, 'rdf_log_path': rdf_log_path}

        return output

    def capsule_experience(self, capsule, create_label=False):
        # type (dict) -> dict
        """
        Main function to register computer vision object and people detections
        Parameters
        ----------
        capsule: dict
            Contains all necessary information regarding the detections.
        create_label: Boolean
            Turn automatic rdfs:label on or off for instance graph entities (people detections)

        Returns
        -------
        capsule: dict
            Returns back the capsule, adding the response code.

        """

        # Process capsule to right types
        capsule['entity'] = self._rdf_builder.fill_entity(casefold_text(capsule['item']['label'], format='triple'),
                                                          capsule['item']['type'] + ['Instance'],
                                                          'LW',
                                                          uri=capsule['item']['uri'])
        capsule['perspective'] = self._rdf_builder.fill_perspective({'certainty': capsule['confidence'],
                                                                     'polarity': 1}) \
            if 'certainty' in capsule.keys() else self._rdf_builder.fill_perspective({'polarity': 1})
        capsule['utterance_type'] = UtteranceType[capsule['utterance_type']] \
            if type(capsule['utterance_type']) == str else capsule['utterance_type']

        # Casefold
        capsule['source']['type'] = [casefold_text(t, format='triple') for t in capsule['source']['type']]
        capsule['item']['type'] = [casefold_text(t, format='triple') for t in capsule['item']['type']]

        # Create graphs and triples
        process_experience(self, capsule, create_label)

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        # Create JSON output
        output = {'response': code, 'experience': capsule, 'rdf_log_path': rdf_log_path}

        return output

    def capsule_mention(self, capsule, reason_types=False, return_thoughts=True, create_label=False):
        # type (dict) -> dict
        """
        Main function to register individual mentions of entities
        Parameters
        ----------
        capsule: dict
            Contains all necessary information regarding the mentions.
        create_label: Boolean
            Turn automatic rdfs:label on or off for instance graph entities

        Returns
        -------
        capsule: dict
            Returns back the capsule, adding the response code.

        """
        # Try to figure out what this entity is
        if reason_types:
            if not capsule['item']['type'] or capsule['item']['type'] == '':
                item_type, _ = self.type_reasoner.reason_entity_type(capsule['item']['label'], exact_only=True)
                capsule['item']['type'] = [item_type]

        # Process capsule to right types
        capsule['entity'] = self._rdf_builder.fill_entity(casefold_text(capsule['item']['label'], format='triple'),
                                                          capsule['item']['type'] + ['Instance'],
                                                          'LW',
                                                          uri=capsule['item']['uri'])
        if type(capsule['utterance_type']) == str:
            capsule['utterance_type'] = UtteranceType[capsule['utterance_type']]

        # Fix perspectives
        if 'perspective' not in capsule.keys():
            capsule['perspective'] = {}
        if capsule['utterance_type'] in (UtteranceType.IMAGE_MENTION, UtteranceType.TEXT_MENTION):
            capsule['perspective']['polarity'] = 1
        capsule['perspective'] = self._rdf_builder.fill_perspective(capsule['perspective'])

        # Casefold
        source = 'author' \
            if capsule['utterance_type'] in (UtteranceType.STATEMENT, UtteranceType.TEXT_MENTION, UtteranceType.TEXT_ATTRIBUTION) \
            else 'source'
        capsule[source]['type'] = [casefold_text(t, format='triple') for t in capsule[source]['type']]
        capsule['item']['type'] = [casefold_text(t, format='triple') for t in capsule['item']['type']]

        # Create graphs and triples
        process_mention(self, capsule, create_label)

        # Check how many items of the same type as subject and complement we have
        if return_thoughts:
            entity_novelty = self.thought_generator.fill_entity_novelty(capsule['entity'].id, capsule['entity'].id)
        else:
            entity_novelty = None

        # Finish process of uploading new knowledge to the triple store
        rdf_log_path = self._brain_log()
        data = self._serialize(rdf_log_path)
        code = self._upload_to_brain(data)

        # Check for gaps, in case we want to be proactive
        if return_thoughts:
            entity_gaps = self.thought_generator.get_entity_gaps(capsule['entity'])
        else:
            entity_gaps = None

        # Create JSON output
        thoughts = Thoughts(None, entity_novelty, None, None, None, entity_gaps, None, None)
        output = {'response': code, 'mention': capsule, 'thoughts': thoughts, 'rdf_log_path': rdf_log_path}

        return output
def main():
    # Initialize LongTermMemory instance with dummy parameters
    scenario_filepath = pathlib.Path('../../data/')
    graph_filepath = scenario_filepath / pathlib.Path('graph/')
    graph_filepath.mkdir(parents=True, exist_ok=True)
    # Create brain connection
    ltm = LongTermMemory(address="http://localhost:7200/repositories/sandbox",  # Location to save accumulated graph
                           log_dir=graph_filepath,  # Location to save step-wise graphs
                           clear_all=True)
    # Context capsule
    # Define contextual features
    from tqdm import tqdm
    from random import getrandbits
    import requests
    from datetime import date, datetime
    context_id = getrandbits(8)
    place_id = getrandbits(8)
    location = requests.get("https://ipinfo.io").json()
    start_date = date(2021, 3, 12)
    context_capsule =  {"context_id": context_id,
     "date": start_date,
     "place": "Carl's room",
     "place_id": place_id,
     "country": location['country'],
     "region": location['region'],
     "city": location['city']}

    response = ltm.capsule_context(context_capsule)

    # Create a sample capsule to test capsule_statement
    sample_capsule_statement =  {  # CARL SAYS CANNOT SEE HIS PILLS
            "chat": 1,
            "turn": 1,
            "author": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/friends/carl-1"},
            "utterance": "I need to take my pills, but I cannot find them.",
            "utterance_type": UtteranceType.STATEMENT,
            "position": "0-25",
            "subject": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/world/carl-1"},
            "predicate": {"label": "see", "uri": "http://cltl.nl/leolani/n2mu/see"},
            "object": {"label": "pills", "type": ["object", "medicine"], 'uri': "http://cltl.nl/leolani/world/pills-1"},
            "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
            "timestamp": datetime.combine(start_date, datetime.now().time()),
            "context_id": context_id
        }
    # Test the capsule_statement function
    print("\nTesting capsule_statement...")
    statement_output = ltm.capsule_statement(
        sample_capsule_statement,
        reason_types=True,
        return_thoughts=True,
        create_label=True
    )

    # Print the output for capsule_statement
    print("Response Code:", statement_output.get('response'))
    print("Statement Processed:", statement_output.get('statement'))
    print("Thoughts:", statement_output.get('thoughts'))
    print("RDF Log Path:", statement_output.get('rdf_log_path'))

    # Create a sample capsule to test capsule_event
    sample_capsule_event = {  # CARL SAYS CANNOT SEE HIS PILLS
        "chat": 1,
        "turn": 1,
        "author": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/friends/carl-1"},
        "utterance": "I need to take my pills, but I cannot find them.",
        "utterance_type": UtteranceType.STATEMENT,
        "position": "0-25",
        "event_details": [
            {"subject": {"label": "lunch", "type": ["Activity"],  "uri": "http://cltl.nl/leolani/world/lunch1"},
            "predicate": {"label": "agent", "uri": "http://cltl.nl/leolani/n2mu/hasAgent"},
            "object": {"label": "carl", "type": ["person"], 'uri': "http://cltl.nl/leolani/world/carl-1"}},
            {"subject": {"label": "lunch", "type": ["Activity"], "uri": "http://cltl.nl/leolani/world/lunch1"},
             "predicate": {"label": "object", "uri": "http://cltl.nl/leolani/n2mu/hasObject"},
             "object": {"label": "apples", "type": ["object", "medicine"], 'uri': "http://cltl.nl/leolani/world/pills-1"}},
            {"subject": {"label": "lunch", "type": ["Activity"], "uri": "http://cltl.nl/leolani/world/lunch1"},
             "predicate": {"label": "location", "uri": "http://cltl.nl/leolani/n2mu/hasPlace"},
             "object": {"label": "home", "type": ["place"], 'uri': "http://cltl.nl/leolani/world/home-1"}},
            {"subject": {"label": "lunch", "type": ["Activity"], "uri": "http://cltl.nl/leolani/world/lunch1"},
             "predicate": {"label": "time", "uri": "http://cltl.nl/leolani/n2mu/hasTime"},
             "object": {"label": "sunday", "type": ["time"], 'uri': "http://cltl.nl/leolani/world/sunday"}}
        ],
        "perspective": {"certainty": 1, "polarity": -1, "sentiment": -1},
        "timestamp": datetime.combine(start_date, datetime.now().time()),
        "context_id": context_id
    }

    # Test the capsule_event function
    print("\nTesting capsule_event...")
    event_output = ltm.capsule_event(
        sample_capsule_event,
        reason_types=True,
        return_thoughts=True,
        create_label=True
    )

    # Print the output for capsule_event
    print("Response Code:", event_output.get('response'))
    print("Event Processed:", event_output.get('statement'))
    print("Thoughts:", event_output.get('thoughts'))
    print("RDF Log Path:", event_output.get('rdf_log_path'))


# Run the main function
if __name__ == "__main__":
    main()