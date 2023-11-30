import requests
from SPARQLWrapper import SPARQLWrapper, JSON


class StoreConnector(object):

    def __init__(self, address, format):
        # type: (str, str) -> StoreConnector
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        self.address = address
        self.format = format

    def upload(self, data):
        """
        Post data to the brain
        :param data: serialized data as string
        :return: response status
        """

        # From serialized string
        post_url = self.address + "/statements"
        response = requests.post(post_url,
                                 data=data.encode('utf-8'),
                                 headers={'Content-Type': 'application/x-' + self.format + '; charset=utf-8'})

        return str(response.status_code)

    def query(self, query, ask=False, post=False):
        """
        Submit a SPARQL query to the triple store, and returning the results as JSON
        Parameters
        ----------
        query: str SPARQL query
        ask: Boolean whether the query returns a Boolean
        post: Boolean whether the query is posting information instead of querying

        Returns
        -------
        response: dictionary query results from triple store

        """
        # Set up connection
        endpoint = self.address
        if post:
            endpoint += '/statements'

        sparql = SPARQLWrapper(endpoint)

        # Response parameters
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        sparql.addParameter('Accept', 'application/sparql-results+json')

        if post:
            sparql.method = 'POST'

        response = sparql.query().convert()

        if ask:
            return response['boolean']
        if post:
            return response
        else:
            return response["results"]["bindings"]

    def export_repository(self):
        """
        Export all data in the brain
        :param
        :return: data in repository, as trig
        """

        # From serialized string
        post_url = self.address + "/statements"
        response = requests.get(post_url,
                                 headers={'Content-Type': 'application/x-' + self.format})

        return str(response.text)
