from rdflib import RDF, RDFS

from cltl.brain.LTM_shared import _link_entity, _link_leolani, create_interaction_graph, create_claim_graph, \
    interlink_graphs
from cltl.brain.utils.helper_functions import get_object_id
from cltl.combot.backend.api.discrete import UtteranceType
from cltl.combot.backend.utils.casefolding import casefold_text


######################################## Helpers for detection processing ########################################


def _link_detections_to_context(self, context, dect, prdt):
    # Bidirectional link to context
    self.interaction_graph.add((context.id, self.namespaces['EPS']['hasDetection'], dect.id))
    self.instance_graph.add((dect.id, self.namespaces['EPS']['hasContext'], context.id))

    # Create detection
    claim = create_claim_graph(self, self.myself, prdt, dect)
    self.claim_graph.add((claim.id, self.namespaces['EPS']['hasContext'], context.id))

    return claim


def _create_detection_mention(self, capsule, subevent):
    mention_unit = 'pixel'
    mention_position = f"{'-'.join([str(i) for i in capsule['region']])}"

    # Mention
    mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
    mention = self._rdf_builder.fill_entity(mention_label, ['Mention', 'Experience'], 'LTa')
    _link_entity(self, mention, self.perspective_graph, create_label=True)

    # Bidirectional link between mention and individual instances
    self.instance_graph.add((capsule['entity'].id, self.namespaces['GAF']['denotedIn'], mention.id))
    self.perspective_graph.add((mention.id, self.namespaces['GAF']['containsDenotation'], capsule['entity'].id))

    return mention


def _create_detection_attribution(self, capsule, mention, claim):
    # Assume detections have positive polarity
    perspective = self._rdf_builder.fill_perspective({'certainty': capsule['confidence'], 'polarity': 1})

    attribution_suffix = f"{perspective.certainty.value}" \
                         f"{perspective.polarity.value}" \
                         f"{perspective.sentiment.value}" \
                         f"{perspective.emotion.value}"

    attribution_label = claim.label + f"_{attribution_suffix}"
    attribution = self._rdf_builder.fill_entity(attribution_label, ['Attribution'], 'LTa')
    _link_entity(self, attribution, self.perspective_graph, create_label=True)

    for typ, val in vars(perspective).items():
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


def create_perspective_graph_for_detections(self, capsule, claim, subevent):
    # Mention
    mention = _create_detection_mention(self, capsule, subevent)

    # Attribution
    attribution = _create_detection_attribution(self, capsule, mention, claim)

    return mention, attribution


def create_object_detection(self, capsule, context, create_label):
    # Subevent
    experience, sensor, use_sensor = create_interaction_graph(self, capsule, UtteranceType.EXPERIENCE, create_label)

    # Detections: objects
    if not set(capsule['item']['type']) & {'', 'unknown', 'none'}:
        # Link detection to graphs
        _link_entity(self, capsule['entity'], self.instance_graph, create_label=True)
        claim = _link_detections_to_context(self, context, capsule['entity'], self._rdf_builder.fill_predicate('see'))

        # Perspective
        mention, attribution = create_perspective_graph_for_detections(self, capsule, claim, experience)
        interlink_graphs(self, mention, sensor, experience, claim, use_sensor)

        # Add id information
        objct_id = self._rdf_builder.fill_literal(capsule['item']['id'], datatype=self.namespaces['XML']['string'])
        self.instance_graph.add((capsule['entity'].id, self.namespaces['N2MU']['id'], objct_id))

        # Open ended learning
        object_type = self._rdf_builder.create_resource_uri('N2MU', 'object')
        for t in capsule['item']['type']:
            learnable_type = self._rdf_builder.create_resource_uri('N2MU', t)
            self.ontology_graph.add((learnable_type, RDFS.subClassOf, object_type))


def create_people_detection(self, capsule, context, create_label):
    # Subevent
    experience, sensor, use_sensor = create_interaction_graph(self, capsule, UtteranceType.EXPERIENCE, create_label)

    # Detections: faces
    if not set(capsule['item']['type']) & {'', 'unknown', 'none'}:
        # Link detection to graphs
        _link_entity(self, capsule['entity'], self.instance_graph, create_label)
        claim = _link_detections_to_context(self, context, capsule['entity'], self._rdf_builder.fill_predicate('see'))

        # Perspective
        mention, attribution = create_perspective_graph_for_detections(self, capsule, claim, experience)
        interlink_graphs(self, mention, sensor, experience, claim, use_sensor)


def create_detection(self, capsule, create_label):
    _link_leolani(self)
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')

    if 'person' in capsule['item']['type']:
        create_people_detection(self, capsule, context, create_label)
    else:
        capsule['entity'].add_types(['object'])
        create_object_detection(self, capsule, context, create_label)
