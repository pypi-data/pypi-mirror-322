from typing import Any, Dict

from proofreading_cli.config import Config
from proofreading_cli.paths import SEARCH_DIMENSION_MAPING

RAW_HITS_DATASET_NAME = "hits.parquet"

GC_API_KEY_ENV = "GC_API_KEY"
INFERENCE_SERVER_API_KEY = "INFERENCE_SERVER_API_KEY"

search_dimension_mapping = Config.load(SEARCH_DIMENSION_MAPING)
SEARCH_DIMENSION_MAPPING_DICT: Dict[
    str, str
] = search_dimension_mapping.search.dimension.mapping.to_dict()

MODEL_VERSION_1 = "model_1"
MODEL_VERSION_2 = "model_2"

EMOJIS: Dict[str, Any] = {"robot": "🤖", "loupe": "🔎", "sneak": "🙈", "disc": "💾"}
