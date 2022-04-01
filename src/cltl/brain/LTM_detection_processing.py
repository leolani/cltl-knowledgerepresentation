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


def _create_detection_mention(self, capsule, subevent, detection):
    scores = [x['confidence'] for x in capsule['objects']] + [x['confidence'] for x in capsule['people']]
    mention_unit = 'pixel'
    mention_position = f"0-{len(scores)}"

    # Mention
    mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
    mention = self._rdf_builder.fill_entity(mention_label, ['Mention', 'Experience'], 'LTa')
    _link_entity(self, mention, self.perspective_graph, create_label=True)

    # Bidirectional link between mention and individual instances
    self.instance_graph.add((detection.id, self.namespaces['GAF']['denotedIn'], mention.id))
    self.perspective_graph.add((mention.id, self.namespaces['GAF']['containsDenotation'], detection.id))

    return mention


def _create_detection_attribution(self, mention, claim, detection_certainty):
    # Assume detections have positive polarity
    perspective = self._rdf_builder.fill_perspective({'certainty': detection_certainty, 'polarity': 1})

    attribution_suffix = f"{perspective.certainty.name}-" \
                         f"{perspective.polarity.name}-" \
                         f"{perspective.sentiment.name}-" \
                         f"{perspective.emotion.name}"

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


def create_perspective_graph_for_detections(self, capsule, claim, subevent, detection, detection_certainty):
    # Mention
    mention = _create_detection_mention(self, capsule, subevent, detection)

    # Attribution
    attribution = _create_detection_attribution(self, mention, claim, detection_certainty)

    return mention, attribution


def create_object_detections(self, capsule, context, create_label):
    # Get ids of existing objects in this location
    memory = self.location_reasoner.get_location_memory(capsule)

    # Detections
    prdt = self._rdf_builder.fill_predicate('see')
    object_type = self._rdf_builder.create_resource_uri('N2MU', 'object')

    # Subevent
    experience, sensor, use_sensor = create_interaction_graph(self, capsule, UtteranceType.EXPERIENCE, create_label)

    # Detections: objects
    for item in capsule['objects']:
        if item['type'].lower() not in ['', 'unknown', 'none', 'person']:
            # Create instance
            mem_id, memory = get_object_id(memory, item['type'])
            objct_id = self._rdf_builder.fill_literal(mem_id, datatype=self.namespaces['XML']['string'])
            objct = self._rdf_builder.fill_entity(casefold_text(f"{item['type']} {objct_id}", format='triple'),
                                                  [casefold_text(item['type'], format='triple'), 'Instance', 'object'],
                                                  'LW')
            self.instance_graph.add((objct.id, self.namespaces['N2MU']['id'], objct_id))

            # Link detection to graphs
            _link_entity(self, objct, self.instance_graph, create_label=True)
            claim = _link_detections_to_context(self, context, objct, prdt)

            # Perspective
            mention, attribution = create_perspective_graph_for_detections(self, capsule, claim, experience,
                                                                           detection=objct,
                                                                           detection_certainty=item['confidence'])
            interlink_graphs(self, mention, sensor, experience, claim, use_sensor)

            # Open ended learning
            learnable_type = self._rdf_builder.create_resource_uri('N2MU',
                                                                   casefold_text(item['type'], format='triple'))
            self.ontology_graph.add((learnable_type, RDFS.subClassOf, object_type))


def create_people_detections(self, capsule, context, create_label):
    # Detections
    prdt = self._rdf_builder.fill_predicate('see')

    # Subevent
    experience, sensor, use_sensor = create_interaction_graph(self, capsule, UtteranceType.EXPERIENCE, create_label)

    # Detections: faces
    for item in capsule['people']:
        if item['name'].lower() not in ['', 'unknown', 'none']:
            # Create instance
            prsn = self._rdf_builder.fill_entity(casefold_text(item['name'], format='triple'),
                                                 ['person', 'Instance'],
                                                 'LW')

            # Link detection to graphs
            _link_entity(self, prsn, self.instance_graph, create_label)
            claim = _link_detections_to_context(self, context, prsn, prdt)

            # Perspective
            mention, attribution = create_perspective_graph_for_detections(self, capsule, claim, experience,
                                                                           detection=prsn,
                                                                           detection_certainty=item['confidence'])
            interlink_graphs(self, mention, sensor, experience, claim, use_sensor)


def create_detections(self, capsule, create_label):
    _link_leolani(self)
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')

    create_object_detections(self, capsule, context, create_label)

    create_people_detections(self, capsule, context, create_label)
