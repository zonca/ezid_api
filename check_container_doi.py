import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

EZID_BASE_URL = "https://ezid.cdlib.org/id"
CONTAINER_IDS: List[str] = [
    "doi:10.5072/FK2/SIMONSOBS-RELEASE-2025",
    "doi:10.5072/FK2/SIMONSOBS-RELEASE-2025-P1",
    "doi:10.5072/FK2/SIMONSOBS-RELEASE-2025-P2",
]


def parse_anvl(body: str) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    for line in body.strip().splitlines():
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def print_relation_fields(metadata: Dict[str, str]):
    print("Relationship fields:")
    for key in sorted(metadata):
        if key.startswith(
            (
                "_target",
                "datacite.relatedidentifier",
                "datacite.relatedidentifiertype",
                "datacite.relationtype",
            )
        ):
            print(f"  {key}: {metadata[key]}")
    print()


def check_container_dois():
    load_dotenv()
    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "EZID_USERNAME and EZID_PASSWORD must be set to check container DOIs."
        )

    for identifier in CONTAINER_IDS:
        url = f"{EZID_BASE_URL}/{identifier}"
        print(f"\nFetching metadata for {identifier} ({url})")
        response = requests.get(url, headers={"Accept": "text/plain"}, auth=(username, password))
        print(f"Status: {response.status_code}")
        print("Full metadata:")
        print(response.text.strip())
        response.raise_for_status()

        metadata = parse_anvl(response.text)
        print_relation_fields(metadata)


if __name__ == "__main__":
    check_container_dois()
