#!/usr/bin/env python3
"""A dependency-free toy experiment for bit-flip noise and 3-qubit repetition code.

This is a pedagogical simulator, not a physical quantum circuit simulator.
It models a classical bit-flip channel to make the error-correction trade-off
visible before moving to a framework such as Qiskit or Cirq.
"""

from __future__ import annotations

import argparse
import random


def noisy_bit(bit: int, flip_probability: float, rng: random.Random) -> int:
    return bit ^ int(rng.random() < flip_probability)


def repetition_code_trial(flip_probability: float, rng: random.Random) -> bool:
    """Return whether majority decoding preserves an encoded zero."""
    received = [noisy_bit(0, flip_probability, rng) for _ in range(3)]
    decoded = int(sum(received) >= 2)
    return decoded == 0


def run(p: float, trials: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    single_success = sum(noisy_bit(0, p, rng) == 0 for _ in range(trials)) / trials
    coded_success = sum(repetition_code_trial(p, rng) for _ in range(trials)) / trials
    return single_success, coded_success


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--probabilities", type=float, nargs="*", default=[0.01, 0.05, 0.10, 0.20, 0.30])
    args = parser.parse_args()
    if args.trials <= 0 or any(not 0 <= p <= 1 for p in args.probabilities):
        raise SystemExit("trials must be positive and probabilities must be between 0 and 1")

    print("Quantum noise simulator (toy bit-flip channel)")
    print("p_flip  single_success  repetition_code_success  improvement")
    for p in args.probabilities:
        single, coded = run(p, args.trials, args.seed)
        print(f"{p:>6.2f}  {single:>14.4%}  {coded:>24.4%}  {coded - single:>10.4%}")


if __name__ == "__main__":
    main()
