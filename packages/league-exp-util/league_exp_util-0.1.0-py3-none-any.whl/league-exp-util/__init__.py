"""
league-exp-util

This package provides utilities for calculating League of Legends experience
points based on game duration and outcomes.

Exposed Functions:
    - win: Calculate XP for a win.
    - loss: Calculate XP for a loss.
    - calc: Calculate XP ranges (loss, win, average) for a game duration.
    - find: Estimate the number of matches needed to reach a target XP goal.
"""

from .exp_calculator import win, loss, calc, find

__all__ = ["win", "loss", "calc", "find"]
__version__ = "0.1.0"
