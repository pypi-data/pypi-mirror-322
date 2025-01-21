from typing import Dict

from bs4 import BeautifulSoup
from proofreading_cli.constants import SEARCH_DIMENSION_MAPPING_DICT


def extract_header_and_body(html_text: str) -> Dict[str, str]:
    """
    Extracts header and body content from HTML text.
    """
    soup = BeautifulSoup(html_text, "html.parser")

    header = soup.header.decode_contents() if soup.header else ""

    if soup.header:
        soup.header.decompose()
    body = str(soup).strip()

    return {"headline": header, "body": body}


def map_hit_item(item: dict) -> Dict[str, str]:
    article = extract_header_and_body(item["markedText"])

    return {
        "hit_id": item["id"],
        "search_query_id": item["searchQuery"]["id"],
        "subscription_id": item["searchQuery"]["subscriptionId"],
        "article_id": item["articleId"],
        "proofreading_type": item["searchQuery"]["productionMetadata"][
            "proofreadingType"
        ],
        "proofreading_timestamp": item["proofreading"]["timestamp"],
        "query": item["searchQuery"]["query"],
        "search_dimension_id": item["searchQuery"]["searchDimensionId"],
        "search_dimension_name": SEARCH_DIMENSION_MAPPING_DICT[
            item["searchQuery"]["searchDimensionId"]
        ],
        "headline": article["headline"],
        "body": article["body"],
        "marked_text": item["markedText"],
        "lectorate_search_term": item["searchQuery"]["lectorateSearchTerm"],
        "proofreading_status": item["proofreading"]["status"],
    }
