# League Experience Utility

This package provides tools to calculate League of Legends experience points based on game duration and outcomes with consideration to First-Win-of-The-Day rewards.

## Installation

```bash
pip install league-exp-util
```
## Usage

```Python
from league_exp_util.exp_calculator import find

result = find(target_xp=5000, game_length=30, fwotd=1)
print(result)  # {'min': 21, 'max': 26, 'avg': 23}
```
