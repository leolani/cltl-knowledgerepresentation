from rdflib import Literal


######################################### Helpers for question processing #########################################


def _is_empty(entry):
    return str(entry).lower() in ['', Literal(''), 'unknown', 'none']


def create_query(self, utterance):
    # Query subject
    if _is_empty(utterance['subject']['label']) or _is_empty(utterance['subject']['uri']):
        query = """
SELECT distinct ?s (group_concat(distinct ?slbl ; separator="|") as ?slabel) 
                ?p ?pOriginal 
                ?o (group_concat(distinct ?olbl ; separator="|") as ?olabel)
                (group_concat(distinct ?authorlabel ; separator="|") as ?authorlabel)
                ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue
WHERE { 
   BIND(<%s> AS ?p).
   BIND(<%s> AS ?o).

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
""" % (utterance['predicate']['uri'],
       utterance['object']['uri'])

    # Query complement
    elif _is_empty(utterance['object']['label']) or _is_empty(utterance['object']['uri']):
        query = """
SELECT distinct ?s (group_concat(distinct ?slbl ; separator="|") as ?slabel) 
                ?p ?pOriginal 
                ?o (group_concat(distinct ?olbl ; separator="|") as ?olabel)
                (group_concat(distinct ?authorlabel ; separator="|") as ?authorlabel)
                ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue
WHERE { 
   BIND(<%s> AS ?s).
   BIND(<%s> AS ?p).      
               
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
""" % (utterance['subject']['uri'],
       utterance['predicate']['uri'])

    # Query existence
    else:
        query = """
SELECT distinct ?s (group_concat(distinct ?slbl ; separator="|") as ?slabel) 
                ?p ?pOriginal 
                ?o (group_concat(distinct ?olbl ; separator="|") as ?olabel)
                (group_concat(distinct ?authorlabel ; separator="|") as ?authorlabel)
                ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue
WHERE { 
   BIND(<%s> AS ?s).
   BIND(<%s> AS ?p).
   BIND(<%s> AS ?o).
            
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
""" % (utterance['subject']['uri'],
       utterance['predicate']['uri'],
       utterance['object']['uri'])

    query = self.query_prefixes + query

    self._log.info("Triple in question: %s", utterance['triple'])

    return query
