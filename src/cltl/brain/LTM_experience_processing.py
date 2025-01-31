from rdflib import RDFS

from cltl.brain.LTM_shared import _link_entity, _link_leolani, create_interaction_graph, create_claim_graph, \
    interlink_graphs, create_perspective_graph


######################################## Helpers for detection processing ########################################


def _link_detections_to_context(self, context, dect, prdt):
    # Bidirectional link to context
    self.interaction_graph.add((context.id, self.namespaces['EPS']['hasDetection'], dect.id))
    self.instance_graph.add((dect.id, self.namespaces['EPS']['hasContext'], context.id))

    # Create detection
    claim = create_claim_graph(self, self.myself, prdt, dect)
    self.claim_graph.add((claim.id, self.namespaces['EPS']['hasContext'], context.id))

    return claim


def create_instance_graph_for_visual(self, capsule, create_label):
    # type (dict, bool) -> None
    """
    Create linked data related to what leolani observes in the world
    Parameters
    ----------
    self:
    capsule: dict
    create_label: bool

    Returns
    -------


    """
    _link_leolani(self)

    # Subject
    capsule['triple'].subject.add_types(['Instance'])
    _link_entity(self, capsule['triple'].subject, self.instance_graph, create_label)

    # Complement
    capsule['triple'].complement.add_types(['Instance'])
    _link_entity(self, capsule['triple'].complement, self.instance_graph, create_label)


def create_instance_graph_for_experience(self, capsule, context, create_label):
    # Detections: objects
    if not set(capsule['item']['type']) & {'', 'unknown', 'none'}:
        # Subevent
        experience, sensor, use_sensor = create_interaction_graph(self, capsule, create_label)

        # Link detection to graphs
        _link_entity(self, capsule['entity'], self.instance_graph, create_label)
        claim = _link_detections_to_context(self, context, capsule['entity'], self._rdf_builder.fill_predicate('see'))

        # Perspective
        mention, attribution = create_perspective_graph(self, capsule, claim, experience)
        interlink_graphs(self, mention, sensor, experience, claim, use_sensor)

        if 'person' not in capsule['item']['type']:
            # Add id information
            objct_id = self._rdf_builder.fill_literal(capsule['item']['id'], datatype=self.namespaces['XML']['string'])
            self.instance_graph.add((capsule['entity'].id, self.namespaces['N2MU']['id'], objct_id))

            # Open ended learning
            object_type = self._rdf_builder.create_resource_uri('N2MU', 'object')
            for t in capsule['item']['type']:
                learnable_type = self._rdf_builder.create_resource_uri('N2MU', t)
                self.ontology_graph.add((learnable_type, RDFS.subClassOf, object_type))


def process_experience(self, capsule, create_label):
    _link_leolani(self)
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')

    if 'person' not in capsule['item']['type']:
        capsule['entity'].add_types(['object'])

    create_instance_graph_for_experience(self, capsule, context, create_label)

    self._log.info(f"Entity in experience: {capsule['entity']}")



def process_visual_relation(self, capsule, create_label):
    # Leolani world (includes instance and claim graphs)
    # #create_instance_graph_for_visual(self, capsule, create_label)
    # claim = create_claim_graph(self, capsule['triple'].subject,
    #                            capsule['triple'].predicate,
    #                            capsule['triple'].complement)

    claim = create_claim_graph(self, capsule['subject'],
                               capsule['predicate'],
                               capsule['object'])

    # Leolani talk (includes interaction and perspective graphs)
    statement, actor, make_friend = create_interaction_graph(self, capsule, create_label)
    mention, attribution = create_perspective_graph(self, capsule, claim, statement)

    # Links across
    interlink_graphs(self, mention, actor, statement, claim, make_friend)

    self._log.info(f"Triple in visual: {capsule['triple']}")

    return claim
