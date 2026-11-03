#!/usr/bin/python3

import argparse
import os
import subprocess
import sys


def apk(arguments: list[str]) -> list[str]:
    "Calls apk with arguments and returns a list of output lines"
    args = ["apk"]
    args.extend(arguments)
    cmd = subprocess.run(args, capture_output=True, encoding="utf-8", check=True)
    return cmd.stdout.splitlines()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--textfile",
        help="File to write output to, instead of stdout",
        type=argparse.FileType("w", encoding="UTF-8"),
    )
    parser.add_argument(
        "--update",
        help="Weather to update APK repository indexes before exporting",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    args = parser.parse_args()

    if args.update:
        apk(["update"])

    installed = apk(["list", "-Iq"])
    upgradeable = apk(["list", "-uq"])
    orphaned = apk(["list", "-Oq"])
    try:
        cache_mtime = os.stat("/var/cache/apk").st_mtime
    except FileNotFoundError:
        cache_mtime = 0

    registry = {
        "installed_packages": {
            "name": "apk_installed_packages",
            "help": "apk packages installed",
            "value": len(installed),
        },
        "upgradeable_packages": {
            "name": "apk_upgradable_packages",
            "help": "apk packages pending update",
            "value": len(upgradeable),
        },
        "orphaned_packages": {
            "name": "apk_orphaned_packages",
            "help": "apk packages that are orphaned",
            "value": len(orphaned),
        },
        "cache_timestamp": {
            "name": "apk_package_cache_timestamp_seconds",
            "help": "apk update last run time",
            "value": cache_mtime,
        },
    }

    output = args.textfile or sys.stdout
    for item in registry.values():
        print(f"# HELP {item['name']} {item['help']}", file=output)
        print(f"# TYPE {item['name']} gauge", file=output)
        print(f"{item['name']} {item['value']}", file=output)


if __name__ == "__main__":
    main()
