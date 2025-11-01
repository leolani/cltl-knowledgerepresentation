from rdflib import Literal


######################################### Helpers for question processing #########################################


def _is_empty(entry):
    if type(entry) == list:
        return entry == [] or str(entry[0]).lower() in ['', Literal(''), 'unknown', 'none']

    else:
        return str(entry).lower() in ['', Literal(''), 'unknown', 'none']


def _is_only_namespace(entry):
    """
    Check if namespace is long version or short version
    Parameters
    ----------
    entry: str

    Returns
    -------

    """
    if ":" in entry:
        # short version
        return str(entry).split("//")[-1] in [':']
    else:
        # long version
        return str(entry)[-1] in ['/', '#']


def _create_filter_clauses(triple_element, element_type="s"):
    """
    Check if a triple element is signaling a filter or binding condition.
    The type refers to s (subject), o (object) or p (predicate)
    Parameters
    ----------
    triple_element: dict
    type: str

    Returns
    -------

    """
    # If no label or type or URI is given, do nothing
    filter_clause = ""

    # If the full URI is given, then bind
    if not _is_empty(triple_element['uri']) and not _is_only_namespace(triple_element['uri']):
        filter_clause = """BIND(<%s> AS ?%s).""" % (triple_element['uri'], element_type)

    # If the URI is given but is only a namespace, then filter by that
    elif not _is_empty(triple_element['uri']) and _is_only_namespace(triple_element['uri']):
        filter_clause = """FILTER (STRSTARTS(str(?%s), "%s")) .""" % (element_type, triple_element['uri'])


    # If the full type is given (short version), then bind (Type filter only makes sense for entities, not predicates)
    elif not _is_empty(triple_element['type']) and not _is_only_namespace(triple_element['type']):
        filter_clause = """?%s rdf:type n2mu:%s .""" % (element_type, triple_element['type'][0])

    # If the type is given (short version) but is only a namespace, then filter by that (Type filter only makes sense for entities, not predicates)
    elif not _is_empty(triple_element['uri']) and  _is_only_namespace(triple_element['type']):
        filter_clause = """?%s rdf:type ?elemt .
                            FILTER (STRSTARTS(str(?elemt), "%s")) .""" % (element_type, triple_element['type'])


    # If the label is given, then filter by that
    elif not _is_empty(triple_element['label']):
        if element_type == "s":
            filter_clause = """FILTER (STRSTARTS(str(?slbl), "%s")) .""" % (triple_element['label'])
        elif element_type == "o":
            filter_clause = """FILTER (STRSTARTS(str(?olbl), "%s")) .""" % (triple_element['label'])
        elif element_type == "p":
            filter_clause = """FILTER (CONTAINS(str(?pOriginal), "%s")) .""" % (triple_element['label'])

    return filter_clause


def create_query(self, utterance):
    # Known subject filter
    subject_filter = _create_filter_clauses(utterance['subject'], element_type="s")

    # Known object filter
    object_filter = _create_filter_clauses(utterance['object'], element_type="o")

    # Check if predicate is empty or signaling a namespace filter
    predicate_filter = _create_filter_clauses(utterance['predicate'], element_type="p")

    query = """
SELECT distinct ?s (group_concat(distinct ?slbl ; separator="|") as ?slabel) 
            ?p ?pOriginal 
            ?o (group_concat(distinct ?olbl ; separator="|") as ?olabel)
            (group_concat(distinct ?authorlabel ; separator="|") as ?authorlabel)
            ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue
WHERE { 
%s
%s
%s
        
?s ?p ?o .
?pOriginal rdfs:subPropertyOf* ?p .

OPTIONAL {
    ?s rdfs:label ?slbl .
    ?o rdfs:label ?olbl .
}

GRAPH ?g {
    ?s ?pOriginal ?o . 
} . 

OPTIONAL {
    ?g gaf:denotedBy ?m . 
    ?m grasp:wasAttributedTo ?author . 
    ?author rdfs:label ?authorlabel .
    ?m grasp:hasAttribution ?att .

    ?att rdf:value ?certainty .
    ?certainty rdf:type graspf:CertaintyValue .
    ?certainty rdfs:label ?certaintyValue .

    ?att rdf:value ?polarity .
    ?polarity rdf:type graspf:PolarityValue .
    ?polarity rdfs:label ?polarityValue .

    ?att rdf:value ?emotion .
    ?emotion rdf:type graspe:EmotionValue .
    ?emotion rdfs:label ?emotionValue .

    ?att rdf:value ?sentiment .
    ?sentiment rdf:type grasps:SentimentValue .
    ?sentiment rdfs:label ?sentimentValue .
}
}
GROUP BY ?s ?p ?pOriginal ?o ?author ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue
""" % (subject_filter, predicate_filter, object_filter)

    query = self.query_prefixes + query

    self._log.info("Triple in question: %s", utterance['triple'])
    self._log.debug("Query became:%s", query)

    return query
