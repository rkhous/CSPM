# CSPM
Crowd-Sourced PokeMap for Monocle

1) Install discord.py using: python3 -m pip install -U discord.py
2) Set up config.py
3) Run with:
    python3 cspm.py

4) Error 2006: `SET GLOBAL max_allowed_packet=10485760;`
    
**Spawns:
Spawns are given a 15 minute timer since the timer is assumed to be unknown. (Your maps will likely have a spawnpoint option though)
Command: .spawn <pokemon_name> <lat> <lon>
Example: .spawn larvitar 34.101085 -118.287312

**Raids (currently no eggs):
Command: .raid <gym_name> <pokemon_name> <raid_level> <minutes_remaining>
Example: .raid "Silverlake Painted" Rayquaza 5 29

Note: Gym names in raids do not have to be completely filled in, just enough so MySQL can find a single gym. 
