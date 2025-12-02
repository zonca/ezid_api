import os
from typing import Iterable, List, Tuple

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


def build_release_metadata() -> List[Tuple[str, List[Tuple[str, str]]]]:
    """Define metadata for a release DOI and its product DOIs."""
    release_id = f"{TEST_SHOULDER}/OCEAN-RELEASE-2025"
    product_1_id = f"{TEST_SHOULDER}/OCEAN-RELEASE-2025-P1"
    product_2_id = f"{TEST_SHOULDER}/OCEAN-RELEASE-2025-P2"

    release = (
        release_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/data-releases/ocean-2025"),
            ("datacite.creator", "Example Marine Lab"),
            ("datacite.title", "2025 Coastal Observing System Data Release"),
            ("datacite.publisher", "Example Marine Lab"),
            ("datacite.publicationyear", "2025"),
            ("datacite.resourcetype", "Collection"),
            ("datacite.relatedidentifier.1", product_1_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "HasPart"),
            ("datacite.relatedidentifier.2", product_2_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.2", "DOI"),
            ("datacite.relationtype.2", "HasPart"),
        ],
    )

    product_1 = (
        product_1_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/data-releases/ocean-2025/sea-surface-temp"),
            ("datacite.creator", "Example Marine Lab"),
            ("datacite.title", "Sea Surface Temperature Gridded Product (2025 Release)"),
            ("datacite.publisher", "Example Marine Lab"),
            ("datacite.publicationyear", "2025"),
            ("datacite.resourcetype", "Dataset"),
            ("datacite.version", "2025.1"),
            ("datacite.relatedidentifier.1", release_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "IsPartOf"),
        ],
    )

    product_2 = (
        product_2_id,
        [
            ("_profile", "datacite"),
            ("_target", "https://example.org/data-releases/ocean-2025/chlorophyll"),
            ("datacite.creator", "Example Marine Lab"),
            ("datacite.title", "Chlorophyll-a Satellite Mosaic (2025 Release)"),
            ("datacite.publisher", "Example Marine Lab"),
            ("datacite.publicationyear", "2025"),
            ("datacite.resourcetype", "Dataset"),
            ("datacite.version", "2025.1"),
            ("datacite.relatedidentifier.1", release_id.split("doi:", 1)[1]),
            ("datacite.relatedidentifiertype.1", "DOI"),
            ("datacite.relationtype.1", "IsPartOf"),
        ],
    )

    return [release, product_1, product_2]


def create_container_and_products():
    """Create a container DOI plus product DOIs that point back to it."""
    load_dotenv()
    username = os.getenv("EZID_USERNAME")
    password = os.getenv("EZID_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "EZID_USERNAME and EZID_PASSWORD must be set in the environment or .env file."
        )

    auth = (username, password)
    for identifier, metadata in build_release_metadata():
        put_identifier(identifier, metadata, auth)
        print(f"Successfully registered {identifier}")
        print(f"Resolve at {doi_url(identifier)}")


if __name__ == "__main__":
    create_container_and_products()
