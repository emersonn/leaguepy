"""
Riot API Connection Manager
Emerson Matson

Used for all requests to the Riot API, including grabbing player data,
    creating a session with the Riot server.

Testing Tips:
    My Player ID: 27284
    Random match: 1932421719
"""

import requests
import warnings

BASE_URL = "https://{location}.api.pvp.net/"

# https://{location}.api.pvp.net/api/lol/{location}/
BASE_API_URL = BASE_URL + "api/lol/{location}/"

# https://{location}.api.pvp.net/api/lol/static-data/{location}/
BASE_STATIC_URL = BASE_URL + "api/lol/static-data/{location}/"

URLS = {
    'ids': BASE_API_URL + 'v1.4/summoner/by-name/{players}',

    'stats': BASE_API_URL + 'v1.3/stats/by-summoner/{player}/ranked/',
    'champion': BASE_STATIC_URL + 'v1.2/champion/{champion}/',

    'featured': BASE_URL + 'observer-mode/rest/featured/',

    'matches': BASE_API_URL + 'v2.2/matchhistory/{player}/',
    'match': BASE_API_URL + 'v2.2/match/{match}/',
    'match_list': BASE_API_URL + 'v2.2/matchlist/by-summoner/{player}/'
}

# TODO(Try abstracting with json.loads in object_hook to make consistent.)

# TODO(Add error checking, error codes, etc. r.status_code = 429.)
#   Rate limiting throw errors.
#   Handle similarly to Tweepy.

# TODO(Streamline the .get() and .format() and add unit tests for such.)


class RiotSession(requests.Session):
    def __init__(self, api, location="na"):
        self.params.update({'api_key': api})
        self.location = location

        super(RiotSession, self).__init__()

    def _get_request(self, connection, formats={}, parameters={}):
        """Builds a request with the given URL key.

        Args:
            connection: Desired URL key in the URLS list.
            formats: Keyword arguments to format the string with.
            parameters: Extra parameters for the .get() request.

        Returns:
            json: JSON loaded response from the server.

        Assumptions:
            Desired location for API server is the current Session's stored
                location.
        """

        if 'location' not in formats:
            formats['location'] = self.location

        return self.get(
            URLS[connection].format(**formats),
            params=parameters
        ).json()

    def get_featured(self):
        """Gets the featured games.

        Returns:
            list: List of featured games. If there are no games in the list,
                an empty list is returned.
        """

        try:
            return self._get_request('featured')['gameList']
        except KeyError:
            return []

    def get_matches(self, player, matches=5, match_type='RANKED_SOLO_5x5'):
        """SOON TO BE REMOVED."""

        warnings.warn("Riot will be depricating this URL.")

        try:
            parameters = {'rankedQueues': match_type, 'endIndex': matches}
            return self._get_request(
                'matches',
                {'player': str(player)},
                parameters
            )['matches']
        except KeyError:
            return []

    def get_match(self, match):
        """Gets a particular match's data.

        Args:
            match (int): Match ID for the particular match.

        Returns:
            json: Match data.
        """

        return self._get_request(
            'match',
            {'match': str(match)}
        )

    # TODO(Unicode encode error.)
    def get_ids(self, players):
        """Gets the IDs from the list of usernames given.

        Args:
            players (list): List of players to perform the lookup on.

        Returns:
            json: List of player IDs.
        """

        return self._get_request(
            'ids',
            {'players': ','.join(players)}
        )

    def get_stats(self, player):
        """Gets the ranked stats of a particular player.

        Args:
            player: Player ID.

        Returns:
            json: Player champion statistics.
        """

        return self._get_request(
            'stats',
            {'player': str(player)}
        )

    def get_match_list(self, player, match_type='RANKED_SOLO_5x5'):
        """Gets the match list of a player.

        Args:
            player: ID of the player.
            match_type: Match types to filter by.
                Defaults to Ranked 5v5 Solo matches.

        Returns:
            list: List of match data.
        """

        parameters = {'rankedQueues': match_type}
        try:
            return self._get_request(
                'match_list',
                {'player': str(player)},
                parameters
            )['matches']
        except KeyError:
            return []

    def get_champion(self, champion_id, champ_data="all"):
        """Gets static champion data.

        Args:
            champion_id: Champion ID.
            champ_data: Riot specific argument.
                Defaults to ALL champion data returned.

        Returns:
            json: Champion data.
        """

        parameters = {'champData': champ_data}
        return self._get_request(
            'champion',
            {'champion': str(champion_id)},
            parameters
        )
