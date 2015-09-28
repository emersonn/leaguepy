# leaguepy
A League of Legends API wrapper. An easy, streamlined way to work with Riot's
developer API.

## Installation
With the setup.py installation is quite easy.

```sh
$ cd path/to/main/folder
$ pip install .
```

## Basic Usage
1. Create a RiotSession object with your API Key and (optional) desired location.
 The location is the key for locations specified in the Riot API.
 Example: "na" or "euw." Argument defaults to "na."

  ```python
  import RiotSession from leaguepy
  SESSION = RiotSession(API_KEY)
 ```
2. Call functions on the SESSION to pull data from Riot's servers.

## Built In Functions
`get_featured()` grabs the featured games.

`get_match(match_id)` grabs a single match.

`get_ids(players)` grabs the ids from a list of usernames.

`get_stats(player)` grabs the summary statistics for a single player.

`get_match_list(player, match_type='RANKED_SOLO_5x5')` grabs the match list
  for a single player.

`get_champion(champion_id, champ_data="all")` grabs the static champion data
  relevant to the champion in question.

## Testing
Testing requires mock, nose and (optional) coverage libraries. Setup.cfg should
allow you to use nosetests right away and ensure leaguepy works in your
environment.
