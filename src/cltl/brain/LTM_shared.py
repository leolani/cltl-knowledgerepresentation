from rdflib import RDF, RDFS, OWL

from cltl.brain.utils.constants import NAMESPACE_MAPPING
from cltl.brain.utils.helper_functions import hash_claim_id
from cltl.combot.backend.api.discrete import UtteranceType


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


def create_interaction_graph(self, capsule, claim_type, create_label):
    # Context
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')

    # Chat or Visual
    event_id = self._rdf_builder.fill_literal(capsule['chat'] if claim_type == UtteranceType.STATEMENT
                                              else capsule['visual'], datatype=self.namespaces['XML']['string'])
    event_type = 'chat' if claim_type == UtteranceType.STATEMENT else 'visual'
    event_label = f'{event_type}{event_id}'
    event = self._rdf_builder.fill_entity(event_label, ['Event', f"{event_type.title()}"], 'LTa')
    _link_entity(self, event, self.interaction_graph, create_label=True)
    self.interaction_graph.add((event.id, self.namespaces['N2MU']['id'], event_id))
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasEvent'], event.id))

    # Utterance or Detection are events and instances
    subevent_id = self._rdf_builder.fill_literal(capsule['turn'] if claim_type == UtteranceType.STATEMENT
                                                 else capsule['detection'], datatype=self.namespaces['XML']['string'])
    subevent_type = 'utterance' if claim_type == UtteranceType.STATEMENT else 'detection'
    subevent_label = f'{str(event.label)}_{subevent_type}{str(subevent_id)}'
    subevent = self._rdf_builder.fill_entity(subevent_label, ['Event', f'{subevent_type.title()}'], 'LTa')
    _link_entity(self, subevent, self.interaction_graph, create_label=True)

    # Actor
    actor, interaction = _create_actor(self, capsule, claim_type, create_label)
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


def interlink_graphs(self, mention, actor, subevent, claim, interaction):
    # Link mention and its properties like actor and event
    self.perspective_graph.add((mention.id, self.namespaces['GRASP']['wasAttributedTo'], actor.id))
    self.perspective_graph.add((mention.id, self.namespaces['PROV']['wasDerivedFrom'], subevent.id))

    # Bidirectional link between mention and claim
    self.claim_graph.add((claim.id, self.namespaces['GAF']['denotedBy'], mention.id))
    self.perspective_graph.add((mention.id, self.namespaces['GAF']['denotes'], claim.id))

    # Link mention to the interaction
    # self.claim_graph.add((interaction.id, self.namespaces['GAF']['denotedBy'], mention.id))
