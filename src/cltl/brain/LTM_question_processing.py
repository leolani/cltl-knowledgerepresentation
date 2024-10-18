from rdflib import Literal


######################################### Helpers for question processing #########################################


def _is_empty(entry):
    return str(entry).lower() in ['', Literal(''), 'unknown', 'none']


def _is_only_namespace(entry):
    return str(entry)[-1] in ['/', '#']


def create_query(self, utterance):
    # Known subject filter
    if _is_empty(utterance['subject']['label']) or _is_empty(utterance['subject']['uri']):
        subject_filter = ""
    else:
        subject_filter = """BIND(<%s> AS ?s).""" % (utterance['subject']['uri'])

    # Known object filter
    if _is_empty(utterance['object']['label']) or _is_empty(utterance['object']['uri']):
        object_filter = ""
    else:
        object_filter = """BIND(<%s> AS ?o).""" % (utterance['object']['uri'])

    # Check if predicate is empty or signaling a namespace filter
    if _is_only_namespace(utterance['predicate']['uri']):
        predicate_filter = """FILTER (STRSTARTS(str(?p), "%s")) .""" % (utterance['predicate']['uri'])
    elif _is_empty(utterance['predicate']['label']) or _is_empty(utterance['predicate']['uri']):
        predicate_filter = ""
    else:
        predicate_filter = """BIND(<%s> AS ?p).""" % (utterance['predicate']['uri'])

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
