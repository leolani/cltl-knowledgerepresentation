from rdflib import RDF

from cltl.brain.LTM_shared import _link_entity, _link_leolani, create_interaction_graph, create_claim_graph, \
    interlink_graphs
from cltl.combot.backend.api.discrete import UtteranceType


######################################## Helpers for statement processing ########################################


def _create_statement_mention(self, capsule, subevent):
    mention_unit = 'char'
    mention_position = f"0-{len(capsule['utterance'])}"
    transcript = self._rdf_builder.fill_literal(capsule['utterance'], datatype=self.namespaces['XML']['string'])

    # Mention
    mention_label = f'{subevent.label}_{mention_unit}{mention_position}'
    mention = self._rdf_builder.fill_entity(mention_label, ['Mention', 'Statement'], 'LTa')
    _link_entity(self, mention, self.perspective_graph, create_label=True)

    # Bidirectional link between mention and individual instances
    self.instance_graph.add((capsule['triple'].subject.id, self.namespaces['GAF']['denotedIn'], mention.id))
    self.instance_graph.add((capsule['triple'].complement.id, self.namespaces['GAF']['denotedIn'], mention.id))
    self.perspective_graph.add(
        (mention.id, self.namespaces['GAF']['containsDenotation'], capsule['triple'].subject.id))
    self.perspective_graph.add(
        (mention.id, self.namespaces['GAF']['containsDenotation'], capsule['triple'].complement.id))
    self.perspective_graph.add((mention.id, RDF.value, transcript))

    return mention


def _create_statement_attribution(self, capsule, mention, claim):
    attribution_suffix = f"{capsule['perspective'].certainty.name}-" \
                         f"{capsule['perspective'].polarity.name}-" \
                         f"{capsule['perspective'].sentiment.name}-" \
                         f"{capsule['perspective'].emotion.name}"

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


def create_perspective_graph_for_statements(self, capsule, claim, subevent):
    # Mention
    mention = _create_statement_mention(self, capsule, subevent)

    # Attribution
    attribution = _create_statement_attribution(self, capsule, mention, claim)

    return mention, attribution


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
    capsule['triple'].subject.add_types(['Instance'])
    _link_entity(self, capsule['triple'].subject, self.instance_graph, create_label)

    # Complement
    capsule['triple'].complement.add_types(['Instance'])
    _link_entity(self, capsule['triple'].complement, self.instance_graph, create_label)


def model_graphs(self, capsule, create_label):
    # Leolani world (includes instance and claim graphs)
    create_instance_graph(self, capsule, create_label)
    claim = create_claim_graph(self, capsule['triple'].subject,
                               capsule['triple'].predicate,
                               capsule['triple'].complement)

    # Leolani talk (includes interaction and perspective graphs)
    statement, actor, make_friend = create_interaction_graph(self, capsule, UtteranceType.STATEMENT, create_label)
    mention, attribution = create_perspective_graph_for_statements(self, capsule, claim, statement)

    # Links across
    interlink_graphs(self, mention, actor, statement, claim, make_friend)

    self._log.info(f"Triple in statement: {capsule['triple']}")

    return claim
