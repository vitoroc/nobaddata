import argparse
import sys

import pandas as pd

from nobaddata.core.engine import Engine
from nobaddata.reporting import reporter
from nobaddata.reporting.console import ConsoleReporter


def main():
    parser = argparse.ArgumentParser(prog="nobaddata")

    parser.add_argument("command", choices=["run"], help="Command to execute")

    parser.add_argument("config", help="Path to YAML config file")

    parser.add_argument("--data", required=True, help="Path to dataset (CSV)")

    parser.add_argument(
        "--fail-only", action="store_true", help="Show only failed or errored checks"
    )

    args = parser.parse_args()

    # IMPORTANT: load checks
    import nobaddata.checks

    if args.command == "run":
        run_command(args)


def run_command(args):
    df = pd.read_csv(args.data)

    engine = Engine.from_yaml(args.config)
    results = engine.run(df)

    reporter = ConsoleReporter()
    status_order = {"ERROR": 0, "FAIL": 1, "PASS": 2}
    severity_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    results.sort(key=lambda r: (status_order[r.status], severity_order[r.severity]))
    reporter.report(results, fail_only=args.fail_only)

    # EXIT CODES
    if any(r.status == "ERROR" for r in results):
        sys.exit(2)
    elif any(r.status == "FAIL" for r in results):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
