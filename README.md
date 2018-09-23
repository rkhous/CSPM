# CSPM

## Crowd-Sourced PokeMap for Monocle

- Install discord.py using: `python3 -m pip install -U discord.py`
- Set up config.py
- Run with: `python3 cspm.py`
- If you run into 'No module named MySQLdb' issues: first run `sudo apt-get install gcc python-dev` followed by `pip3 install mysqlclient`

    
## Spawns:
- Spawns are given a 15 minute timer since the timer is assumed to be unknown. (Your maps will likely have a spawnpoint option though)
- Command: ```.spawn <pokemon_name> <lat> <lon>```
- Example: ```.spawn larvitar 34.101085 -118.287312```

## Raids *(currently no eggs)*:
- Command: ```.raid <gym_name> <pokemon_name> <raid_level> <minutes_remaining>```
- Example: ```.raid "Silverlake Painted" Rayquaza 5 29```

- Note: Gym names in raids do not have to be completely filled in, just enough so MySQL can find a single gym.

## Quests *(currently no map support)*:
- Command: ```.quest <stop_name> <quest_type> <quest_reward>```
- Example: ```.quest "Fishermans Warf" "Complete a Raid" "Dratini"```

## Searching for gyms and stops:
- Command: ```.search <gym/pokestop> <name>```
- Example: ```.search gym starbucks```
- Example: ```.search pokestop sprint```

- Note: Gym/Pokestop names do not have to be completely filled in. Searching for 'tarbuck' will still show all gyms with with that string in them!

## Other
- [Support the development, if you'd like](http://paypal.me/rkhous)
- [Join my Discord](https://discord.gg/FDbSR9K)
