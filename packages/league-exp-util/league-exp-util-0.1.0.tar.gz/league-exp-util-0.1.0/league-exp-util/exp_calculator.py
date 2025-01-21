"""
exp_calculator.py

This module calculates the experience points (XP) earned in Summoner's Rift
matches based on game duration and win/loss results. It also estimates the
number of matches needed to reach a target XP goal.

Dependencies:
    - math: Used for ceiling calculations.

Functions:
    - win: Calculate XP earned for winning a match.
    - loss: Calculate XP earned for losing a match.
    - calc: Provide XP ranges (low, high, average) for a game duration.
    - find: Estimate matches needed to reach a target XP goal.
"""

import math


def win(game_seconds: int) -> int:
    """
    Calculate the XP rewarded for winning a PvP match on Summoner's Rift.


    Args:
        game_seconds (int): The number of seconds the game has elapsed.

    Returns:
        int: Match XP rewarded.

    Example:
        >>> win(100)
        18
    """
    xp = round((game_seconds*0.11)+6.6)
    return xp


def loss(game_seconds: int) -> int:
    """
    Calculate the XP rewarded for losing a PvP match on Summoner's Rift.

    Args:
        game_seconds (int): The number of seconds the game has elapsed.

    Returns:
        int: Match XP rewarded for a loss.

    Example:
        >>> loss(100)
        14
    """
    xp = round((game_seconds*0.09)+5.4)
    return xp


def calc(game_duration_minutes: float) -> dict[str, int]:
    """
    Calculate XP ranges (high, low, and average) for a given game duration.

    Args:
        game_duration_minutes (float): Game duration in minutes.

    Returns:
        dict: A dictionary containing:
            - "loss": XP for a loss.
            - "win": XP for a win.
            - "avg": Average XP for win and loss.

    Example:
        >>> calc(35)
        {'high': 238, 'low': 194, 'avg': 216}
    """
    game_duration_seconds = round(game_duration_minutes*60)
    low = loss(game_duration_seconds)
    high = win(game_duration_seconds)
    average = round((low+high)/2)
    d = {"loss": low,
         "win": high,
         "avg": average}
    return d


def find(
        target_xp: int,
        game_length: int = 35,
        fwotd: int = 0,
        ) -> dict[str, int]:
    """
    Estimate the number of matches needed to reach a target XP goal.

    Args:
        target_xp (int): The total XP goal.
        game_length (int): Average game duration in minutes (default: 35).
        fwotd (int): Number of First Win of the Day bonuses (400 XP each).

    Returns:
        dict: A dictionary with the number of matches needed for:
            - "min": Matches assuming maximum XP per game.
            - "max": Matches assuming minimum XP per game.
            - "avg": Matches assuming average XP.

    Raises:
        ValueError: If `target_xp` is less than or equal to 0.
        ValueError: If `fwotd` is negative.

    Example:
        >>> find(5000, game_length=30, fwotd=2)
        {'min': 21, 'max': 26, 'avg': 23}
    """
    if fwotd < 0:
        raise ValueError("fwotd must be non-negative")
    if target_xp <= 0:
        raise ValueError("target_xp must be greater than 0")

    target_xp -= 400*fwotd
    xp_per_game = calc(game_length)
    for k in xp_per_game:
        xp_per_game[k] = math.ceil(target_xp/xp_per_game[k])
    matches_needed = {
        "min": xp_per_game["win"],
        "max": xp_per_game["loss"],
        "avg": xp_per_game["avg"]
    }
    return matches_needed
