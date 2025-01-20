import os
from blue_options.env import load_config, load_env

load_env(__name__)
load_config(__name__)


DAMAGES_TEST_DATASET_OBJECT_NAME = os.getenv(
    "DAMAGES_TEST_DATASET_OBJECT_NAME",
    "",
)

ENCODED_BLOB_SAS_TOKEN = os.getenv("ENCODED_BLOB_SAS_TOKEN", "")

SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_debug_v2 = os.getenv(
    "SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_debug_v2",
    "",
)

SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_full_v2 = os.getenv(
    "SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_full_v2",
    "",
)

PALISADES_QUERY_OBJECT_PALISADES_MAXAR = os.getenv(
    "PALISADES_QUERY_OBJECT_PALISADES_MAXAR",
    "",
)

PALISADES_QUERY_OBJECT_PALISADES_MAXAR_TEST = os.getenv(
    "PALISADES_QUERY_OBJECT_PALISADES_MAXAR_TEST",
    "",
)
