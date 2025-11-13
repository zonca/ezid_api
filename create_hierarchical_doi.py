import os
from typing import Iterable, Tuple

import requests
from dotenv import load_dotenv

EZID_BASE_URL = "https://ezid.cdlib.org/id"
TEST_SHOULDER = "doi:10.5072/FK2"


def to_anvl(metadata_items: Iterable[Tuple[str, str]]) -> str:
    """Convert ordered metadata pairs to ANVL formatted text."""
    return "".join(f"{key}: {value}\n" for key, value in metadata_items)


def doi_url(identifier: str) -> str:
    """Return the https://doi.org/... URL from an EZID identifier string."""
    suffix = identifier.split(":", 1)[1] if identifier.startswith("doi:") else identifier
    return f"https://doi.org/{suffix}"


def put_identifier(identifier: str, metadata_items: Iterable[Tuple[str, str]], auth):
    """Send a PUT request to EZID for the provided identifier."""
    url = f"{EZID_BASE_URL}/{identifier}"
    payload = to_anvl(metadata_items).encode("utf-8")
    headers = {"Content-Type": "text/plain", "Accept": "text/plain"}

    print(f"\nDOI landing page: {doi_url(identifier)}")
    response = requests.put(url, data=payload, headers=headers, auth=auth)
    print(f"Request to {url}")
    print(payload.decode("utf-8"))
    print(f"Status: {response.status_code}")
    print(f"Response:\n{response.text}")
    response.raise_for_status()


def build_hierarchy_metadata():
    """Define metadata for canonical and version-specific DOIs."""
    canonical_id = f"{TEST_SHOULDER}/WORK-ALL"
    version1_id = f"{TEST_SHOULDER}/WORK-V1"
    version2_id = f"{TEST_SHOULDER}/WORK-V2"

    canonical = (
        canonical_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/datasets/work-all"),
            ("datacite.creator", "Institutional Research Group"),
            ("datacite.title", "My Dataset on Family & Crime (all versions)"),
            ("datacite.publisher", "Example University"),
            ("datacite.publicationyear", "2025"),
            ("datacite.resourcetype", "Dataset"),
            ("datacite.version", "all"),
            ("datacite.relatedidentifier.1", version1_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "HasVersion"),
            ("datacite.relatedidentifier.2", version2_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.2", "DOI"),
            ("datacite.relationtype.2", "HasVersion"),
        ],
    )

    version_1 = (
        version1_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/datasets/work-v1"),
            ("datacite.creator", "Institutional Research Group"),
            ("datacite.title", "My Dataset on Family & Crime (version 1.0)"),
            ("datacite.publisher", "Example University"),
            ("datacite.publicationyear", "2024"),
            ("datacite.resourcetype", "Dataset"),
            ("datacite.version", "1.0"),
            ("datacite.relatedidentifier.1", canonical_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "IsVersionOf"),
            ("datacite.relatedidentifier.2", version2_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.2", "DOI"),
            ("datacite.relationtype.2", "IsPreviousVersionOf"),
        ],
    )

    version_2 = (
        version2_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/datasets/work-v2"),
            ("datacite.creator", "Institutional Research Group"),
            ("datacite.title", "My Dataset on Family & Crime (version 2.0)"),
            ("datacite.publisher", "Example University"),
            ("datacite.publicationyear", "2025"),
            ("datacite.resourcetype", "Dataset"),
            ("datacite.version", "2.0"),
            ("datacite.relatedidentifier.1", canonical_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "IsVersionOf"),
            ("datacite.relatedidentifier.2", version1_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.2", "DOI"),
            ("datacite.relationtype.2", "IsNewVersionOf"),
        ],
    )

    return [canonical, version_1, version_2]


def create_hierarchical_dois():
    load_dotenv()
    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "EZID_USERNAME and EZID_PASSWORD must be set in the environment or .env file."
        )

    auth = (username, password)
    for identifier, metadata in build_hierarchy_metadata():
        put_identifier(identifier, metadata, auth)
        print(f"Successfully registered {identifier}")
        print(f"Resolve at {doi_url(identifier)}")


if __name__ == "__main__":
    create_hierarchical_dois()
