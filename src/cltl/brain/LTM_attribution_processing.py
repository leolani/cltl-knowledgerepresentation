from cltl.brain.LTM_shared import _link_entity, _link_leolani, create_interaction_graph, create_perspective_graph, \
    interlink_graphs


######################################## Helpers for attribution processing ########################################


def create_instance_graph_for_attribution(self, capsule, create_label):
    # Detections: objects
    if not set(capsule['item']['type']) & {'', 'unknown', 'none'}:
        # Subevent
        experience, sensor, use_sensor = create_interaction_graph(self, capsule, create_label)

        # Link detection to graphs
        _link_entity(self, capsule['entity'], self.instance_graph, create_label)

        # Mention
        mention, attribution = create_perspective_graph(self, capsule, None, experience)
        interlink_graphs(self, mention, sensor, experience, None, use_sensor)

        if 'person' not in capsule['item']['type']:
            # Add id information
            objct_id = self._rdf_builder.fill_literal(capsule['item']['id'], datatype=self.namespaces['XML']['string'])
            self.instance_graph.add((capsule['entity'].id, self.namespaces['N2MU']['id'], objct_id))


def process_attribution(self, capsule, create_label):
    _link_leolani(self)

    create_instance_graph_for_attribution(self, capsule, create_label)

    self._log.info(f"Entity in attribution: {capsule['entity']}")
