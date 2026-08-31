import argparse
from dataclasses import asdict
import json

from .stats import summarize


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize timing samples")
    parser.add_argument("samples", nargs="+", type=float)
    args = parser.parse_args()
    print(json.dumps(asdict(summarize(args.samples)), indent=2))


if __name__ == "__main__":
    main()

