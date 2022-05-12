from random import getrandbits

from cltl.brain.LTM_shared import _link_entity
from cltl.combot.backend.utils.casefolding import casefold_text


def _create_time(self, capsule, context):
    # Time
    time = self._rdf_builder.fill_entity(capsule['date'].strftime('%Y-%m-%d'), ['Time', 'DateTimeDescription'], 'LC')
    _link_entity(self, time, self.interaction_graph, create_label=True)
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasBeginTimeStamp'], time.id))

    # Set specifics of datetime
    day = self._rdf_builder.fill_literal(capsule['date'].day, datatype=self.namespaces['XML']['gDay'])
    month = self._rdf_builder.fill_literal(capsule['date'].month, datatype=self.namespaces['XML']['gMonthDay'])
    year = self._rdf_builder.fill_literal(capsule['date'].year, datatype=self.namespaces['XML']['gYear'])
    time_unit = self._rdf_builder.create_resource_uri('TIME', 'unitDay')
    self.interaction_graph.add((time.id, self.namespaces['TIME']['day'], day))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['month'], month))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['year'], year))
    self.interaction_graph.add((time.id, self.namespaces['TIME']['unitType'], time_unit))


def _create_place(self, capsule, context):
    # City level
    location_city = self._rdf_builder.fill_entity(capsule['city'], ['location', 'city', 'Place'], 'LW')
    _link_entity(self, location_city, self.interaction_graph, create_label=True)
    # Country level
    location_country = self._rdf_builder.fill_entity(capsule['country'], ['location', 'country', 'Place'], 'LW')
    _link_entity(self, location_country, self.interaction_graph, create_label=True)
    # Region level
    location_region = self._rdf_builder.fill_entity(capsule['region'], ['location', 'region', 'Place'], 'LW')
    _link_entity(self, location_region, self.interaction_graph, create_label=True)

    # Create location
    if capsule['place'] is None or capsule['place'].lower() in ['', 'unknown', 'none']:
        # All unknowns have label Unknown and different ids. Their iri is linked to their context
        location_label = casefold_text(f"Unknown", format='triple')
        uri_suffix = casefold_text(f"UNKNOWN{capsule['context_id']}", format='triple')
        location_uri = self._rdf_builder.create_resource_uri('LC', uri_suffix)
        location = self._rdf_builder.fill_entity(location_label, ['location', 'Place'], 'LC', uri=location_uri)

        if capsule['place_id'] is None:
            capsule['place_id'] = getrandbits(8)

    else:
        location_label = casefold_text(f"{capsule['place']}", format='triple')
        location = self._rdf_builder.fill_entity(location_label, ['location', 'Place'], 'LC')

        if capsule['place_id'] is None:
            # If hospital exists and has an id then use that id, if it does not exist then add id
            ids = self.get_id_of_instance(location.id)
            if ids:
                capsule['place_id'] = ids[0]
            else:
                capsule['place_id'] = getrandbits(8)

    location_id = self._rdf_builder.fill_literal(capsule['place_id'], datatype=self.namespaces['XML']['string'])

    _link_entity(self, location, self.interaction_graph, create_label=True)
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['id'], location_id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_city.id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_country.id))
    self.interaction_graph.add((location.id, self.namespaces['N2MU']['in'], location_region.id))
    self.interaction_graph.add((context.id, self.namespaces['SEM']['hasPlace'], location.id))


def process_context(self, capsule):
    # Create an episodic awareness by making a context
    context_id = self._rdf_builder.fill_literal(capsule['context_id'], datatype=self.namespaces['XML']['string'])
    context = self._rdf_builder.fill_entity(f"context{capsule['context_id']}", ['Context'], 'LC')
    _link_entity(self, context, self.interaction_graph, create_label=True)
    self.interaction_graph.add((context.id, self.namespaces['N2MU']['id'], context_id))

    # Time
    _create_time(self, capsule, context)

    # Place
    _create_place(self, capsule, context)

    self._log.info(f"Context: {context}")

    return context
