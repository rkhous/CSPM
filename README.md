# CSPM
Crowd-Sourced PokeMap for Monocle

1. Install [pipenv](https://docs.pipenv.org/)
2. Install mysql 
    * `brew install mysql`
3. Checkout repository
    * `git clone ...`
4. Setup dependencies
    * `cd CSPM`
    * `pipenv install`
5. Run inside pipenv
    * `pipenv run cspm.py`

**Error 2006: `SET GLOBAL max_allowed_packet=10485760;`
    
**Spawns:
Spawns are given a 15 minute timer since the timer is assumed to be unknown. (Your maps will likely have a spawnpoint option though)
Command: .spawn <pokemon_name> <lat> <lon>
Example: .spawn larvitar 34.101085 -118.287312

**Raids (currently no eggs):
Command: .raid <gym_name> <pokemon_name> <raid_level> <minutes_remaining>
Example: .raid "Silverlake Painted" Rayquaza 5 29

Note: Gym names in raids do not have to be completely filled in, just enough so MySQL can find a single gym. 
