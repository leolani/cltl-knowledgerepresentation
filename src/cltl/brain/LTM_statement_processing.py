from random import getrandbits

from rdflib import RDF, RDFS, OWL

from cltl.brain.utils.constants import NAMESPACE_MAPPING
from cltl.brain.utils.helper_functions import hash_claim_id, get_object_id, \
    confidence_to_certainty_value
from cltl.combot.backend.api.discrete import UtteranceType
from cltl.combot.backend.utils.casefolding import casefold_text


######################################## Helpers for statement processing ########################################
def _link_leolani(self):
    if self.myself is None:
        # Create Leolani
        self.myself = self._rdf_builder.fill_entity('leolani', ['robot'], 'LW')

    _link_entity(self, self.myself, self.instance_graph, create_label=True)


def _link_entity(self, entity, graph, create_label, namespace_mapping=None):
    # Set basics like label
    if create_label:
        graph.add((entity.id, RDFS.label, entity.label))

    # Set types
    if entity.types == ['']:  # We only get the label
        entity_type = self._rdf_builder.create_resource_uri(OWL, 'Thing')
        graph.add((entity.id, RDF.type, entity_type))

    else:
        namespace_mapping = NAMESPACE_MAPPING \
            if namespace_mapping is None else namespace_mapping.update(NAMESPACE_MAPPING)

        for item in entity.types:
            entity_type = self._rdf_builder.create_resource_uri(namespace_mapping.get(item, 'N2MU'), item)
            graph.add((entity.id, RDF.type, entity_type))


def _link_detections(self, context, dect, prdt):
    # Bidirectional link to context
    self.interaction_graph.add((context.id, self.namespaces['EPS']['hasDetection'], dect.id))
    self.instance_graph.add((dect.id, self.namespaces['EPS']['hasContext'], context.id))
    # Create detection
    detection = create_claim_graph(self, self.myself, prdt, dect)
    self.claim_graph.add((detection.id, self.namespaces['EPS']['hasContext'], context.id))

    return detection


def _create_detections(self, capsule, context, create_label):
    # Get ids of existing objects in this location
    memory = self.location_reasoner.get_location_memory(capsule)

    # Detections: objects
    _link_leolani(self)
    prdt = self._rdf_builder.fill_predicate('see')
    object_type = self._rdf_builder.create_resource_uri('N2MU', 'object')
    instances = []
    observations = []

    for item in capsule['objects']:
        if item['type'].lower() not in ['', 'unknown', 'none', 'person']:
            # Create instance
            mem_id, memory = get_object_id(memory, item['type'])
            objct_id = self._rdf_builder.fill_literal(mem_id, datatype=self.namespaces['XML']['string'])
            objct = self._rdf_builder.fill_entity(casefold_text(f"{item['type']} {objct_id}", format='triple'),
                                                  [casefold_text(item['type'], format='triple'), 'Instance', 'object'],
                                                  'LW')

            # Link detection to graph
            _link_entity(self, objct, self.instance_graph, create_label=True)
            self.interaction_graph.add((objct.id, self.namespaces['N2MU']['id'], objct_id))
            instances.append(objct)

            # Link to context
            detection = _link_detections(self, context, objct, prdt)
            observations.append(detection)

            # Open ended learning
            learnable_type = self._rdf_builder.create_resource_uri('N2MU',
                                                                   casefold_text(item['type'], format='triple'))
            self.ontology_graph.add((learnable_type, RDFS.subClassOf, object_type))

    # Detections: faces
    for item in capsule['people']:
        if item['name'].lower() not in ['', 'unknown', 'none']:
            # Create instance
            prsn = self._rdf_builder.fill_entity(casefold_text(item['name'], format='triple'),
                                                 ['person', 'Instance'],
                                                 'LW')

            # Link detection to graph
            _link_entity(self, prsn, self.instance_graph, create_label)
            instances.append(prsn)

            # Link to context
            detection = _link_detections(self, context, prsn, prdt)
            observations.append(detection)

    return instances, observations


def _create_context(self, capsule, create_label):
    # Create an episodic awareness by making a context
    context_id = self._rdf_builder.fill_literal(capsule['context_id'], datatype=self.namespaces['XML']['string'])
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')
    _link_entity(self, context, self.interaction_graph, create_label=True)
    self.interaction_graph.add((context.id, self.namespaces['N2MU']['id'], context_id))

    # Time
    time = self._rdf_builder.fill_entity(capsule['date'].strftime('%Y-%m-%d'), ['Time', 'DateTimeDescription'], 'LC')
    _link_entity(self, time, self.interaction_graph, create_label=True)
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasBeginTimeStamp'], time.id))

    # Set specifics of datetime
    day = self._rdf_builder.fill_literal(capsule['date'].day, datatype=self.namespaces['XML']['gDay'])
    month = self._rdf_builder.fill_literal(capsule['date'].month, datatype=self.namespaces['XML']['gMonthDay'])
    year = self._rdf_builder.fill_literal(capsule['date'].year, datatype=self.namespaces['XML']['gYear'])
    time_unit = self._rdf_builder.create_resource_uri('TIME', 'unitDay')
    self.interaction_graph.add((time.id, self.namespaces['TIME']['day'], day))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['month'], month))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['year'], year))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['unitType'], time_unit))

    # City level
    location_city = self._rdf_builder.fill_entity(capsule['city'], ['location', 'city', 'Place'], 'LW')
    _link_entity(self, location_city, self.interaction_graph, create_label=True)
    # Country level
    location_country = self._rdf_builder.fill_entity(capsule['country'], ['location', 'country', 'Place'], 'LW')
    _link_entity(self, location_country, self.interaction_graph, create_label=True)
    # Region level
    location_region = self._rdf_builder.fill_entity(capsule['region'], ['location', 'region', 'Place'], 'LW')
    _link_entity(self, location_region, self.interaction_graph, create_label=True)

    # Create location
    if capsule['place'] is None or capsule['place'].lower() in ['', 'unknown', 'none']:
        # All unknowns have label Unknown and different ids. Their iri is linked to their context
        location_label = casefold_text(f"Unknown", format='triple')
        uri_suffix = casefold_text(f"UNKNOWN{capsule['context_id']}", format='triple')
        location_uri = self._rdf_builder.create_resource_uri('LC', uri_suffix)
        location = self._rdf_builder.fill_entity(location_label, ['location', 'Place'], 'LC', uri=location_uri)

        if capsule['place_id'] is None:
            capsule['place_id'] = getrandbits(8)

    else:
        location_label = casefold_text(f"{capsule['place']}", format='triple')
        location = self._rdf_builder.fill_entity(location_label, ['location', 'Place'], 'LC')

        if capsule['place_id'] is None:
            # If hospital exists and has an id then use that id, if it does not exist then add id
            ids = self.get_id_of_instance(location.id)
            if ids:
                capsule['place_id'] = ids[0]
            else:
                capsule['place_id'] = getrandbits(8)

    location_id = self._rdf_builder.fill_literal(capsule['place_id'], datatype=self.namespaces['XML']['string'])

    _link_entity(self, location, self.interaction_graph, create_label=True)
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['id'], location_id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_city.id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_country.id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_region.id))
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasPlace'], location.id))

    # Detections
    instances, observations = _create_detections(self, capsule, context, create_label)

    return context, instances, observations


def _create_actor(self, utterance, claim_type, create_label):
    if claim_type == UtteranceType.STATEMENT:
        source = utterance['author']
        source_type = 'person'
        ns = 'LF'
        pred = 'know'

    else:
        source = 'front-camera'
        source_type = 'sensor'
        ns = 'LI'
        pred = 'sense'

    # Actor
    actor = self._rdf_builder.fill_entity(source, ['Instance', 'Source', 'Actor', source_type], ns)
    _link_entity(self, actor, self.interaction_graph, create_label=True)

    # Add leolani knows/senses actor
    predicate = self._rdf_builder.fill_predicate(pred)
    interaction = create_claim_graph(self, self.myself, predicate, actor)

    # Add actor (friend) is same as person(world)
    if 'person' in actor.types:
        person = self._rdf_builder.fill_entity(f"{actor.label}", ['Instance', 'person'], 'LW')
        _link_entity(self, person, self.instance_graph, create_label)
        self.claim_graph.add((actor.id, OWL.sameAs, person.id))

    return actor, interaction


def _create_events(self, utterance, claim_type, context, create_label):
    # Chat or Visual
    event_id = self._rdf_builder.fill_literal(utterance['chat'], datatype=self.namespaces['XML']['string'])
    event_type = 'chat' if claim_type == UtteranceType.STATEMENT else 'visual'
    event_label = f'{event_type}{event_id}'
    event = self._rdf_builder.fill_entity(event_label, ['Event', f"{event_type.title()}"], 'LTa')
    _link_entity(self, event, self.interaction_graph, create_label=True)
    self.interaction_graph.add((event.id, self.namespaces['N2MU']['id'], event_id))
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasEvent'], event.id))

    # Utterance or Detection are events and instances
    subevent_id = self._rdf_builder.fill_literal(utterance['turn'], datatype=self.namespaces['XML']['string'])
    subevent_type = 'utterance' if claim_type == UtteranceType.STATEMENT else 'detection'
    subevent_label = f'{str(event.label)}_{subevent_type}{str(subevent_id)}'
    subevent = self._rdf_builder.fill_entity(subevent_label, ['Event', f'{subevent_type.title()}'], 'LTa')
    _link_entity(self, subevent, self.interaction_graph, create_label=True)

    # Actor
    actor, interaction = _create_actor(self, utterance, claim_type, create_label)
    self.interaction_graph.add((subevent.id, self.namespaces['N2MU']['id'], subevent_id))
    self.interaction_graph.add((subevent.id, self.namespaces['SEM']['hasActor'], actor.id))
    self.interaction_graph.add((event.id, self.namespaces['SEM']['hasSubEvent'], subevent.id))

    return subevent, actor, interaction


def _create_mention(self, utterance, subevent, claim_type, detection):
    if claim_type == UtteranceType.STATEMENT:
        mention_unit = 'char'
        mention_position = f"0-{len(utterance['utterance'])}"
        transcript = self._rdf_builder.fill_literal(utterance['utterance'], datatype=self.namespaces['XML']['string'])
    else:
        scores = [x['confidence'] for x in utterance['objects']] + [x['confidence'] for x in utterance['people']]
        mention_unit = 'pixel'
        mention_position = f"0-{len(scores)}"

    # Mention
    mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
    mention = self._rdf_builder.fill_entity(mention_label, ['Mention', claim_type.name.title()], 'LTa')
    _link_entity(self, mention, self.perspective_graph, create_label=True)

    # Bidirectional link between mention and individual instances
    if claim_type == UtteranceType.STATEMENT:
        self.instance_graph.add((utterance['triple'].subject.id, self.namespaces['GAF']['denotedIn'], mention.id))
        self.instance_graph.add((utterance['triple'].complement.id, self.namespaces['GAF']['denotedIn'], mention.id))
        self.perspective_graph.add(
            (mention.id, self.namespaces['GAF']['containsDenotation'], utterance['triple'].subject.id))
        self.perspective_graph.add(
            (mention.id, self.namespaces['GAF']['containsDenotation'], utterance['triple'].complement.id))
        self.perspective_graph.add((mention.id, RDF.value, transcript))
    else:
        self.instance_graph.add((detection.id, self.namespaces['GAF']['denotedIn'], mention.id))
        self.perspective_graph.add((mention.id, self.namespaces['GAF']['containsDenotation'], detection.id))

    return mention


def _create_attribution(self, capsule, mention, claim, claim_type=None):
    if claim_type == UtteranceType.STATEMENT:
        attribution_suffix = f"{capsule['perspective'].certainty.name}-" \
                             f"{capsule['perspective'].polarity.name}-" \
                             f"{capsule['perspective'].sentiment.name}-" \
                             f"{capsule['perspective'].emotion.name}"
    else:
        scores = [x['confidence'] for x in capsule['objects']] + [x['confidence'] for x in capsule['people']]
        certainty_value = confidence_to_certainty_value(sum(scores) / float(len(scores)))
        attribution_suffix = f"{certainty_value}"

    attribution_label = claim.label + f"_{attribution_suffix}"
    attribution = self._rdf_builder.fill_entity(attribution_label, ['Attribution'], 'LTa')
    _link_entity(self, attribution, self.perspective_graph, create_label=True)

    for typ, val in vars(capsule['perspective']).items():
        if val is None:
            continue

        if typ in ['_factuality', '_certainty', '_time', '_polarity']:
            ns = 'GRASPf'
        elif typ in ['_sentiment']:
            ns = 'GRASPs'
        elif typ in ['_emotion']:
            ns = 'GRASPe'
        else:
            ns = 'GRASP'

        attribution_value = self._rdf_builder.fill_entity(val.name, ['AttributionValue', f"{typ[1:].title()}Value"], ns)
        _link_entity(self, attribution_value, self.perspective_graph, create_label=True)
        self.perspective_graph.add((attribution.id, RDF.value, attribution_value.id))

    # Bidirectional link between mention and attribution
    self.perspective_graph.add((mention.id, self.namespaces['GRASP']['hasAttribution'], attribution.id))
    self.perspective_graph.add((attribution.id, self.namespaces['GRASP']['isAttributionFor'], mention.id))

    return attribution


def create_instance_graph(self, capsule, create_label):
    # type (Utterance) -> Graph, Graph, str, str, str
    """
    Create linked data related to what leolani learned/knows about the world
    Parameters
    ----------
    self:
    capsule: dict
    create_label: bool

    Returns
    -------
    claim: claim graph


    """
    _link_leolani(self)
    # Subject
    if capsule['utterance_type'] == UtteranceType.STATEMENT:
        capsule['triple'].subject.add_types(['Instance'])
        _link_entity(self, capsule['triple'].subject, self.instance_graph, create_label)

    elif capsule['utterance_type'] == UtteranceType.EXPERIENCE:
        _link_leolani(self)

    # Complement
    capsule['triple'].complement.add_types(['Instance'])
    _link_entity(self, capsule['triple'].complement, self.instance_graph, create_label)

    # Claim graph
    predicate = capsule['triple'].predicate if capsule['utterance_type'] == UtteranceType.STATEMENT \
        else self._rdf_builder.fill_predicate('see')

    claim = create_claim_graph(self, capsule['triple'].subject, predicate, capsule['triple'].complement)

    return claim


def create_claim_graph(self, subject, predicate, complement):
    # Statement
    claim_label = hash_claim_id([subject.id.split('/')[-1], predicate.label, complement.id.split('/')[-1]])
    claim = self._rdf_builder.fill_entity(claim_label, ['Event', 'Assertion'], 'LW')
    _link_entity(self, claim, self.claim_graph, create_label=True)

    # Create graph and add triple
    graph = self.dataset.graph(claim.id)
    graph.add((subject.id, predicate.id, complement.id))

    return claim


def create_interaction_graph(self, capsule, claim, create_label):
    # Add context
    context, detections, observations = _create_context(self, capsule, create_label)

    # Subevent
    experience, sensor, use_sensor = _create_events(self, capsule, UtteranceType.EXPERIENCE, context, create_label)
    for detection, observation in zip(detections, observations):
        mention, attribution = create_perspective_graph(self, capsule, claim, experience, UtteranceType.EXPERIENCE,
                                                        detection=detection)
        interlink_graphs(self, mention, sensor, experience, observation, use_sensor)

    if capsule['utterance_type'] == UtteranceType.STATEMENT:
        statement, actor, make_friend = _create_events(self, capsule, UtteranceType.STATEMENT, context, create_label)
        mention, attribution = create_perspective_graph(self, capsule, claim, statement, UtteranceType.STATEMENT)
        interlink_graphs(self, mention, actor, statement, claim, make_friend)


def create_perspective_graph(self, utterance, claim, subevent, claim_type, detection=None):
    # Mention
    mention = _create_mention(self, utterance, subevent, claim_type, detection=detection)

    # Attribution
    attribution = _create_attribution(self, utterance, mention, claim, claim_type=claim_type)

    return mention, attribution


def interlink_graphs(self, mention, actor, subevent, claim, interaction):
    # Link mention and its properties like actor and event
    self.perspective_graph.add((mention.id, self.namespaces['GRASP']['wasAttributedTo'], actor.id))
    self.perspective_graph.add((mention.id, self.namespaces['PROV']['wasDerivedFrom'], subevent.id))

    # Bidirectional link between mention and claim
    self.claim_graph.add((claim.id, self.namespaces['GAF']['denotedBy'], mention.id))
    self.perspective_graph.add((mention.id, self.namespaces['GAF']['denotes'], claim.id))

    # Link mention to the interaction
    # self.claim_graph.add((interaction.id, self.namespaces['GAF']['denotedBy'], mention.id))


def model_graphs(self, capsule, create_label):
    # Leolani world (includes instance and claim graphs)
    claim = create_instance_graph(self, capsule, create_label)

    # Leolani talk (includes interaction and perspective graphs)
    create_interaction_graph(self, capsule, claim, create_label)

    self._log.info(f"Triple in statement: {capsule['triple']}")

    return claim
