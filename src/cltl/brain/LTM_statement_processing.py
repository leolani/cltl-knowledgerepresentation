from cltl.brain.LTM_shared import _link_entity, _link_leolani, create_interaction_graph, create_claim_graph, \
    interlink_graphs, create_perspective_graph


######################################## Helpers for statement processing ########################################


def create_instance_graph_for_statement(self, capsule, create_label):
    # type (dict, bool) -> None
    """
    Create linked data related to what leolani learned/knows about the world
    Parameters
    ----------
    self:
    capsule: dict
    create_label: bool

    Returns
    -------


    """
    _link_leolani(self) # Todo: do we need to this every time or can we add only on certain cases (e.g empty graph)

    # Subject
    capsule['triple'].subject.add_types(['Instance'])
    _link_entity(self, capsule['triple'].subject, self.instance_graph, create_label)

    # Complement
    capsule['triple'].complement.add_types(['Instance'])
    _link_entity(self, capsule['triple'].complement, self.instance_graph, create_label)

def create_event(self, capsule, create_label):
    for element in capsule["event_details"]:
        # Subject
        element['subject'].add_types(['Instance'])
        _link_entity(self, capsule['subject'], self.instance_graph, create_label)

        # Complement
        element['object'].add_types(['Instance'])
        _link_entity(self, capsule['object'], self.instance_graph, create_label)

def process_statement(self, capsule, create_label):
    # Leolani world (includes instance and claim graphs)
    create_instance_graph_for_statement(self, capsule, create_label)

    # if the capsule has "event_details"
    if "event_details" in capsule.keys():
        create_event(self, capsule, create_label)
        claim = create_claim_graph(self, capsule['triple'].subject,
                                   capsule['triple'].predicate,
                                   capsule['triple'].complement,
                                   event_details=capsule["event_details"])
    else:
        claim = create_claim_graph(self, capsule['triple'].subject,
                                   capsule['triple'].predicate,
                                   capsule['triple'].complement)

    # Leolani talk (includes interaction and perspective graphs)
    statement, actor, make_friend = create_interaction_graph(self, capsule, create_label)
    mention, attribution = create_perspective_graph(self, capsule, claim, statement)

    # Links across
    interlink_graphs(self, mention, actor, statement, claim, make_friend)

    self._log.info(f"Triple in statement: {capsule['triple']}")

    return claim
