from rdflib import Literal


######################################### Helpers for question processing #########################################


def _is_empty(entry):
    return str(entry).lower() in ['', Literal(''), 'unknown', 'none']


def create_query(self, utterance):
    # Query subject
    if _is_empty(utterance['subject']['label']) or _is_empty(utterance['subject']['uri']):
        query = """
        SELECT distinct ?p ?pOriginal ?s ?slabel ?o ?olabel 
                        ?authorlabel ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue ?temporalValue
           WHERE { 
               BIND(<%s> AS ?p).
               BIND(<%s> AS ?o).

               ?s ?p ?o .
               ?pOriginal rdfs:subPropertyOf* ?p .

               OPTIONAL {
                ?s rdfs:label ?slabel .
                ?o rdfs:label ?olabel .
               }

               GRAPH ?g {
                   ?s ?pOriginal ?o . 
               } . 
               
               OPTIONAL {
               ?g gaf:denotedBy ?m . 
               ?m grasp:wasAttributedTo ?author . 
               ?author rdfs:label ?authorlabel .
               ?m grasp:hasAttribution ?att .
               }

               OPTIONAL {
               ?att rdf:value ?certainty .
               ?certainty rdf:type graspf:CertaintyValue .
               ?certainty rdfs:label ?certaintyValue .
               }

               OPTIONAL {
               ?att rdf:value ?polarity .
               ?polarity rdf:type graspf:PolarityValue .
               ?polarity rdfs:label ?polarityValue .
               }

               OPTIONAL {
               ?att rdf:value ?temporal .
               ?temporal rdf:type graspf:TemporalValue .
               ?temporal rdfs:label ?temporalValue .
               }

               OPTIONAL {
               ?att rdf:value ?emotion .
               ?emotion rdf:type graspe:EmotionValue .
               ?emotion rdfs:label ?emotionValue .
               }

               OPTIONAL {
               ?att rdf:value ?sentiment .
               ?sentiment rdf:type grasps:SentimentValue .
               ?sentiment rdfs:label ?sentimentValue .
               }
           }
           """ % (utterance['predicate']['uri'],
                  utterance['object']['uri'])

    # Query complement
    elif _is_empty(utterance['object']['label']) or _is_empty(utterance['object']['uri']):
        query = """
        SELECT distinct ?p ?pOriginal ?s ?slabel ?o ?olabel 
                        ?authorlabel ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue ?temporalValue
           WHERE { 
               BIND(<%s> AS ?s).
               BIND(<%s> AS ?p).
            
               ?s ?p ?o .
               ?pOriginal rdfs:subPropertyOf* ?p .
                
               OPTIONAL {
                ?s rdfs:label ?slabel .
                ?o rdfs:label ?olabel .
               }
               
               GRAPH ?g {
                   ?s ?pOriginal ?o . 
               } . 
               
               OPTIONAL {
               ?g gaf:denotedBy ?m . 
               ?m grasp:wasAttributedTo ?author . 
               ?author rdfs:label ?authorlabel .
               ?m grasp:hasAttribution ?att .
               }
               
               OPTIONAL {
               ?att rdf:value ?certainty .
               ?certainty rdf:type graspf:CertaintyValue .
               ?certainty rdfs:label ?certaintyValue .
               }

               OPTIONAL {
               ?att rdf:value ?polarity .
               ?polarity rdf:type graspf:PolarityValue .
               ?polarity rdfs:label ?polarityValue .
               }

               OPTIONAL {
               ?att rdf:value ?temporal .
               ?temporal rdf:type graspf:TemporalValue .
               ?temporal rdfs:label ?temporalValue .
               }

               OPTIONAL {
               ?att rdf:value ?emotion .
               ?emotion rdf:type graspe:EmotionValue .
               ?emotion rdfs:label ?emotionValue .
               }

               OPTIONAL {
               ?att rdf:value ?sentiment .
               ?sentiment rdf:type grasps:SentimentValue .
               ?sentiment rdfs:label ?sentimentValue .
               }
           }
           """ % (utterance['subject']['uri'],
                  utterance['predicate']['uri'])

    # Query existence
    else:
        query = """
        SELECT distinct ?p ?pOriginal ?s ?slabel ?o ?olabel 
                        ?authorlabel ?certaintyValue ?polarityValue ?sentimentValue ?emotionValue ?temporalValue
           WHERE { 
               BIND(<%s> AS ?s).
               BIND(<%s> AS ?p).
               BIND(<%s> AS ?o).
            
               ?s ?p ?o .
               ?pOriginal rdfs:subPropertyOf* ?p .
                
               OPTIONAL {
                ?s rdfs:label ?slabel .
                ?o rdfs:label ?olabel .
               }
               
               GRAPH ?g {
                   ?s ?pOriginal ?o . 
               } . 
               
               OPTIONAL {
               ?g gaf:denotedBy ?m . 
               ?m grasp:wasAttributedTo ?author . 
               ?author rdfs:label ?authorlabel .
               ?m grasp:hasAttribution ?att .
               }
               
               OPTIONAL {
               ?att rdf:value ?certainty .
               ?certainty rdf:type graspf:CertaintyValue .
               ?certainty rdfs:label ?certaintyValue .
               }

               OPTIONAL {
               ?att rdf:value ?polarity .
               ?polarity rdf:type graspf:PolarityValue .
               ?polarity rdfs:label ?polarityValue .
               }

               OPTIONAL {
               ?att rdf:value ?temporal .
               ?temporal rdf:type graspf:TemporalValue .
               ?temporal rdfs:label ?temporalValue .
               }

               OPTIONAL {
               ?att rdf:value ?emotion .
               ?emotion rdf:type graspe:EmotionValue .
               ?emotion rdfs:label ?emotionValue .
               }

               OPTIONAL {
               ?att rdf:value ?sentiment .
               ?sentiment rdf:type grasps:SentimentValue .
               ?sentiment rdfs:label ?sentimentValue .
               }
           }
           """ % (utterance['subject']['uri'],
                  utterance['predicate']['uri'],
                  utterance['object']['uri'])

    query = self.query_prefixes + query

    self._log.info("Triple in question: %s", utterance['triple'])
    # print(query)

    return query
