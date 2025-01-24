import argparse
import math
from typing import *

__all__ = ["logitfunction", "main"]


def logitfunction(x: float) -> float:
    "This function is the logit function."
    if not (0.0 < x < 1.0):
        return float("nan")
    q = x / (1 - x)
    ans = math.log(q)
    return ans


def main(args: Optional[Iterable] = None) -> None:
    "This function provides the CLI for the logit function."
    if args is not None:
        args = [str(x) for x in args]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "x", type=float, help="This argument is passed to the logit function."
    )
    ns = parser.parse_args(args)
    ans = logitfunction(ns.x)
    print(ans)
