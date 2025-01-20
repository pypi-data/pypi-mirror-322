"""AttackIQ Platform API Utilities

This package provides utility functions for interacting with the AttackIQ Platform API.
"""

__version__ = "0.1.11"

# Define what should be exposed at package level
__all__ = [  # Core client and utility classes
    "AttackIQRestClient",
    "AssessmentUtils",
    "AssetUtils",
    "ResultsUtils",
    "TagUtils",
    "TaggedItemUtils",
    "PhaseResultsUtils",
    "PhaseLogsUtils",
    "AttackIQLogger",
    "AssetStatus",
    # Use case modules
    "assessment_use_cases",
    "asset_use_cases",
    "integration_use_cases",
    "phase_log_use_cases",
    "phase_results_use_cases",
    "result_use_cases",
    "tag_use_cases",
]

# Then import all submodules
from . import assessment_use_cases
from . import asset_use_cases
from . import integration_use_cases
from . import phase_log_use_cases
from . import phase_results_use_cases
from . import result_use_cases
from . import tag_use_cases

# Import key utilities from common_utils first
from .common_utils import (
    AttackIQRestClient,
    AssessmentUtils,
    AssetUtils,
    ResultsUtils,
    TagUtils,
    TaggedItemUtils,
    PhaseResultsUtils,
    PhaseLogsUtils,
    AttackIQLogger,
    AssetStatus,
)
