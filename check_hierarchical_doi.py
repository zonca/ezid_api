import os
from typing import Dict

import requests
from dotenv import load_dotenv

EZID_BASE_URL = "https://ezid.cdlib.org/id"
HIERARCHY_IDS = [
    "doi:10.5072/FK2/WORK-ALL",
    "doi:10.5072/FK2/WORK-V1",
    "doi:10.5072/FK2/WORK-V2",
]


def parse_anvl(body: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    for line in body.strip().splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def print_version_fields(metadata: Dict[str, str]):
    print("Version-related fields:")
    for key in sorted(metadata):
        if key.startswith(
            (
                "datacite.version",
                "datacite.relatedidentifier",
                "datacite.relatedidentifiertype",
                "datacite.relationtype",
            )
        ):
            print(f"  {key}: {metadata[key]}")
    print()


def check_hierarchical_dois():
    load_dotenv()
    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "EZID_USERNAME and EZID_PASSWORD must be set to check hierarchical DOIs."
        )

    for identifier in HIERARCHY_IDS:
        url = f"{EZID_BASE_URL}/{identifier}"
        print(f"\nFetching metadata for {identifier} ({url})")
        response = requests.get(url, headers={"Accept": "text/plain"}, auth=(username, password))
        print(f"Status: {response.status_code}")
        print("Full metadata:")
        print(response.text.strip())
        response.raise_for_status()

        metadata = parse_anvl(response.text)
        print_version_fields(metadata)


if __name__ == "__main__":
    check_hierarchical_dois()
