import os
import re
import textwrap
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import click
import pandas as pd
from proofreading_cli.constants import GC_API_KEY_ENV, INFERENCE_SERVER_API_KEY


def validate_date(ctx: Any, param: Any, value: str) -> str:
    if value is not None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise click.BadParameter(
                f"Invalid date format: '{value}'. Expected format: YYYY-MM-DD."
            )
    return value


def is_api_key_missing_from_env() -> bool:
    return (GC_API_KEY_ENV not in os.environ) or (
        INFERENCE_SERVER_API_KEY not in os.environ
    )


def is_start_date_after_end_date(start_date: str, end_date: str) -> bool:
    return bool(start_date and end_date and start_date > end_date)


def build_filters(
    article_id: str,
    subscription_id: str,
    statuses: Tuple[str],
    is_submitted: bool,
    date_type: str,
    start_date: str,
    end_date: str,
) -> Dict[str, str]:
    filters = {}

    if article_id:
        filters["article-id"] = article_id
    if subscription_id:
        filters["subscription-id"] = subscription_id
    if statuses:
        filters["statuses"] = statuses
    if is_submitted is not None:
        filters["is-submitted"] = is_submitted
    if date_type:
        filters["date-type"] = date_type
    if start_date:
        filters["start-date"] = convert_to_datetime_format(start_date)
    if end_date:
        filters["end-date"] = convert_to_datetime_format(end_date)

    return filters


def build_cli_options(
    file_system: str, inference: Tuple[str], sneak_peek: bool
) -> Dict[str, str]:
    cli_options = {
        "file-system": file_system,
        "inference": list(inference) if "None" not in inference else ["None"],
        "sneak-peek": sneak_peek,
    }
    return cli_options


def format_table(
    header: List[str], data: Optional[Dict[str, str]]
) -> Tuple[List[str], List[str]]:
    table_header = [click.style(head, fg="yellow", bold=True) for head in header]

    if data is None:
        table_data = []
    else:
        table_data = [
            [click.style(key, fg="yellow"), click.style(value, fg="yellow")]
            for key, value in data.items()
        ]

    return table_header, table_data


def wrap_text_in_df(df: pd.DataFrame, width: int) -> pd.DataFrame:
    for col in df.columns:
        df[col] = df[col].apply(lambda x: "\n".join(textwrap.wrap(str(x), width)))
    return df


def exclude_missing_cols(cols: pd.Index, columns_to_select: List[str]) -> List[str]:
    return [col for col in columns_to_select if col in cols]


def convert_to_datetime_format(date_str: str) -> str:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_date
