from cltl.commons.casefolding import casefold_text
from cltl.commons.discrete import UtteranceType
from rdflib import RDF, RDFS, OWL

from cltl.brain.utils.constants import NAMESPACE_MAPPING
from cltl.brain.utils.helper_functions import hash_claim_id


######################################## Helpers for context processing ########################################

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


def _create_actor(self, capsule, create_label):
    if capsule['utterance_type'] in (UtteranceType.STATEMENT, UtteranceType.TEXT_MENTION):
        source = 'author'
        ns = 'LF'
        pred = 'know'

    else:
        source = 'source'
        ns = 'LI'
        pred = 'sense'

    # Actor
    actor = self._rdf_builder.fill_entity(casefold_text(capsule[source]['label'], format='triple'),
                                          capsule[source]['type'] + ['Instance', 'Source', 'Actor'],
                                          ns,
                                          uri=capsule[source]['uri'])
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


def _create_mention(self, capsule, subevent):
    if capsule['utterance_type'] in (UtteranceType.STATEMENT, UtteranceType.TEXT_MENTION):
        mention_unit = 'char'
        mention_position = f"{capsule['position']}"
        timestamp = self._rdf_builder.fill_literal(str(capsule['timestamp']), datatype=self.namespaces['XML']['string'])

        # Mention
        mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
        mention = self._rdf_builder.fill_entity(mention_label, ['Mention', 'Statement'], 'LTa')
        _link_entity(self, mention, self.perspective_graph, create_label=True)

        # Bidirectional link between mention and individual instances
        if capsule['utterance_type'] == UtteranceType.STATEMENT:
            self.instance_graph.add((capsule['triple'].subject.id, self.namespaces['GAF']['denotedIn'], mention.id))
            self.instance_graph.add((capsule['triple'].complement.id, self.namespaces['GAF']['denotedIn'], mention.id))
            self.perspective_graph.add(
                (mention.id, self.namespaces['GAF']['containsDenotation'], capsule['triple'].subject.id))
            self.perspective_graph.add(
                (mention.id, self.namespaces['GAF']['containsDenotation'], capsule['triple'].complement.id))

            transcript = self._rdf_builder.fill_literal(capsule['utterance'], datatype=self.namespaces['XML']['string'])
            self.perspective_graph.add((mention.id, RDF.value, transcript))
        else:
            self.instance_graph.add((capsule['entity'].id, self.namespaces['GAF']['denotedIn'], mention.id))
            self.perspective_graph.add((mention.id, self.namespaces['GAF']['containsDenotation'], capsule['entity'].id))

        self.perspective_graph.add((mention.id, self.namespaces['SEM']['hasBeginTimeStamp'], timestamp))

    else:
        mention_unit = 'pixel'
        mention_position = f"{'-'.join([str(i) for i in capsule['region']])}"
        timestamp = self._rdf_builder.fill_literal(str(capsule['timestamp']), datatype=self.namespaces['XML']['string'])

        # Mention
        mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
        mention = self._rdf_builder.fill_entity(mention_label, ['Mention', 'Experience'], 'LTa')
        _link_entity(self, mention, self.perspective_graph, create_label=True)

        # Bidirectional link between mention and individual instances
        self.instance_graph.add((capsule['entity'].id, self.namespaces['GAF']['denotedIn'], mention.id))
        self.perspective_graph.add((mention.id, self.namespaces['GAF']['containsDenotation'], capsule['entity'].id))
        self.perspective_graph.add((mention.id, self.namespaces['SEM']['hasBeginTimeStamp'], timestamp))

    return mention


def _create_attribution(self, capsule, mention, claim):
    attribution_suffix = f"{capsule['perspective'].certainty.value}" \
                         f"{capsule['perspective'].polarity.value}" \
                         f"{capsule['perspective'].sentiment.value}" \
                         f"{capsule['perspective'].emotion.value}"

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

        attribution_value = self._rdf_builder.fill_entity(val.name,
                                                          ['AttributionValue', f"{typ[1:].title()}Value"],
                                                          ns)
        _link_entity(self, attribution_value, self.perspective_graph, create_label=True)
        self.perspective_graph.add((attribution.id, RDF.value, attribution_value.id))

    # Bidirectional link between mention and attribution
    self.perspective_graph.add((mention.id, self.namespaces['GRASP']['hasAttribution'], attribution.id))
    self.perspective_graph.add((attribution.id, self.namespaces['GRASP']['isAttributionFor'], mention.id))

    return attribution


def create_interaction_graph(self, capsule, create_label):
    # Context
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')

    # Chat or Visual
    event_type = 'chat' \
        if capsule['utterance_type'] in (UtteranceType.STATEMENT, UtteranceType.TEXT_MENTION) else 'visual'
    event_id = self._rdf_builder.fill_literal(capsule[event_type], datatype=self.namespaces['XML']['string'])
    event_label = f'{event_type}{event_id}'
    event = self._rdf_builder.fill_entity(event_label, ['Event', f"{event_type.title()}"], 'LTa')
    _link_entity(self, event, self.interaction_graph, create_label=True)
    self.interaction_graph.add((event.id, self.namespaces['N2MU']['id'], event_id))
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasEvent'], event.id))

    # Utterance or Detection are events and instances
    subevent_type = 'utterance' \
        if capsule['utterance_type'] in (UtteranceType.STATEMENT, UtteranceType.TEXT_MENTION) else 'detection'
    subevent_id = self._rdf_builder.fill_literal(capsule['turn']
                                                 if capsule['utterance_type'] in (UtteranceType.STATEMENT,
                                                                                  UtteranceType.TEXT_MENTION)
                                                 else capsule['detection'], datatype=self.namespaces['XML']['string'])
    subevent_label = f'{str(event.label)}_{subevent_type}{str(subevent_id)}'
    subevent = self._rdf_builder.fill_entity(subevent_label, ['Event', f'{subevent_type.title()}'], 'LTa')
    _link_entity(self, subevent, self.interaction_graph, create_label=True)

    # Actor
    actor, interaction = _create_actor(self, capsule, create_label)
    self.interaction_graph.add((subevent.id, self.namespaces['N2MU']['id'], subevent_id))
    self.interaction_graph.add((subevent.id, self.namespaces['SEM']['hasActor'], actor.id))
    self.interaction_graph.add((event.id, self.namespaces['SEM']['hasSubEvent'], subevent.id))

    return subevent, actor, interaction


def create_claim_graph(self, subject, predicate, complement):
    # Create claim as entity
    claim_label = hash_claim_id([subject.id.split('/')[-1], predicate.label, complement.id.split('/')[-1]])
    claim = self._rdf_builder.fill_entity(claim_label, ['Event', 'Assertion'], 'LW')
    _link_entity(self, claim, self.claim_graph, create_label=True)

    # Create claim as graph and add triple
    graph = self.dataset.graph(claim.id)
    graph.add((subject.id, predicate.id, complement.id))

    return claim


def create_perspective_graph(self, capsule, claim, subevent):
    # Mention
    mention = _create_mention(self, capsule, subevent)

    # Attribution
    attribution = _create_attribution(self, capsule, mention, claim)

    return mention, attribution


def interlink_graphs(self, mention, actor, subevent, claim, interaction):
    # Link mention and its properties like actor and event
    self.perspective_graph.add((mention.id, self.namespaces['GRASP']['wasAttributedTo'], actor.id))
    self.perspective_graph.add((mention.id, self.namespaces['PROV']['wasDerivedFrom'], subevent.id))

    if claim:
        # Bidirectional link between mention and claim
        self.claim_graph.add((claim.id, self.namespaces['GAF']['denotedBy'], mention.id))
        self.perspective_graph.add((mention.id, self.namespaces['GAF']['denotes'], claim.id))

    # Link mention to the interaction
    # self.claim_graph.add((interaction.id, self.namespaces['GAF']['denotedBy'], mention.id))
