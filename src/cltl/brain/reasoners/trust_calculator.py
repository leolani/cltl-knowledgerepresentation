import pathlib

from cltl.brain.basic_brain import BasicBrain
from cltl.brain.utils.helper_functions import read_query, sigmoid


class TrustCalculator(BasicBrain):

    def __init__(self, address, log_dir, clear_all=False):
        # type: (str, pathlib.Path, bool) -> None
        """
        Interact with Triple store

        Parameters
        ----------
        address: str
            IP address and port of the Triple store
        """

        super(TrustCalculator, self).__init__(address, log_dir, clear_all, is_submodule=True)

    def get_trust(self, speaker_uri):
        """
        Get trust level (between 1 and 0) of a friend. Default is set to 0.5
        :return:
        """
        query = read_query('trust/trust_by') % speaker_uri
        response = self._submit_query(query)

        if response and response[0] != {}:
            trust = response[0]['trust']['value']
        else:
            trust = 0.5

        return trust

    def compute_trust(self, speaker_uri, max_chats, mean_novelty, mean_conflicts):
        """
        Compute a value of trust based on what is know about and via this person
        Parameters
        ----------
        speaker_uri: str
            source to be evaluated

        max_chats: float
            maximum chats with a speaker, for normalization purposes

        mean_novelty: float
            average novel statements per speaker, for normalization purposes

        mean_conflicts: float
            average conflicts per speaker, for normalization purposes

        Returns
        -------
        trust_value: float
            Weighted average of features
        """

        # chat based feature
        num_chats = self.count_chat_with(speaker_uri)
        chat_feature = num_chats / max_chats

        # new content feature
        novel_claims = float(len(self.novel_statements_by(speaker_uri)))
        claims_feature = sigmoid(mean_novelty - novel_claims, growth_rate=mean_novelty if mean_novelty > 1 else 1)

        # conflicts feature
        my_conflicts = float(len(self.get_conflicts_by(speaker_uri)))
        conflicts_feature = sigmoid(mean_conflicts - my_conflicts,
                                    growth_rate=mean_conflicts if mean_conflicts > 1 else 1)

        # Aggregate
        trust_value = (chat_feature + claims_feature + conflicts_feature) / 3

        return trust_value

    def delete_trust_network(self):
        """
        Delete the trust values for all known friends
        :return:
        """
        query = read_query('trust/delete_trust')
        _ = self._connection.query(query, post=True)

    def compute_trust_network(self):
        """
        Compute the trust values for all known friends
        Returns
        -------

        """
        self.delete_trust_network()

        # General grain parameters
        friends = self.get_my_friends()
        num_friends = float(len(friends))

        if num_friends > 0:

            best_friends = self.get_best_friends()
            max_chats = float(best_friends[0][1]) if best_friends else 0

            if max_chats > 0:

                num_claims = self.count_statements()
                mean_novelty = num_claims / num_friends if num_friends > 0 else num_claims

                num_conflicts = float(len(self.get_all_negation_conflicts()))
                mean_conflicts = num_conflicts / num_friends if num_friends > 0 else num_conflicts

                for friend in friends:
                    # Form actor
                    actor = self._rdf_builder.fill_entity(friend, ['Instance', 'Source', 'Actor', 'person'], 'LF')

                    # Compute trust
                    trust_in_friend = self.compute_trust(actor.id, max_chats, mean_novelty, mean_conflicts)
                    trust = self._rdf_builder.fill_literal(trust_in_friend, datatype=self.namespaces['XML']['float'])

                    # Structure knowledge
                    self.interaction_graph.add((actor.id, self.namespaces['N2MU']['hasTrustworthinessLevel'], trust))

                # Finish process of uploading new knowledge to the triple store
                data = self._serialize(self._brain_log())
                _ = self._upload_to_brain(data)

        self._log.info("Computed trust for all known agents")
