# Example notebook: https://colab.research.google.com/drive/1GTL1QvEfbBbX-W1uGLbsnngQIlKbqPnC?usp=sharing
import itertools
import os
from typing import Optional

from aiq_platform_api.common_utils import (
    AttackIQRestClient,
    AttackIQLogger,
    PhaseLogsUtils,
    AssessmentUtils,
)
from aiq_platform_api.env import ATTACKIQ_API_TOKEN, ATTACKIQ_PLATFORM_URL

logger = AttackIQLogger.get_logger(__name__)


def list_phase_logs(
    client: AttackIQRestClient,
    scenario_job_id: str,
    limit: Optional[int] = 10,
):
    logger.info(f"Listing phase logs for scenario job ID: {scenario_job_id}...")
    count = 0
    logs = PhaseLogsUtils.get_phase_logs(
        client,
        scenario_job_id=scenario_job_id,
    )
    for log in itertools.islice(logs, limit):
        count += 1
        logger.info(f"Phase Log {count}:")
        logger.info(f"  Log ID: {log.get('id')}")
        logger.info(f"  Trace Type: {log.get('trace_type')}")
        logger.info(f"  Result Summary ID: {log.get('result_summary_id')}")
        logger.info(f"  Created: {log.get('created')}")
        logger.info(f"  Modified: {log.get('modified')}")
        logger.info(f"  Message: {log.get('message')}")
        logger.info("---")
    logger.info(f"Total phase logs listed: {count}")


def get_assessment_results(
    client: AttackIQRestClient, assessment_id: str, limit: int = 10
):
    results_generator = AssessmentUtils.get_assessment_results(client, assessment_id)
    results = [result for result in itertools.islice(results_generator, limit)]
    logger.info(f"Fetched {len(results)} results for assessment ID: {assessment_id}")
    return results


def main():
    client = AttackIQRestClient(ATTACKIQ_PLATFORM_URL, ATTACKIQ_API_TOKEN)
    assessment_id = os.environ.get("ATTACKIQ_ASSESSMENT_ID")
    if assessment_id:
        assessment_results = get_assessment_results(client, assessment_id)
        if assessment_results:
            for assessment_result in assessment_results:
                scenario_job_id = assessment_result.get("scenario_job_id")
                if scenario_job_id:
                    list_phase_logs(client, scenario_job_id)
    else:
        logger.error("ATTACKIQ_ASSESSMENT_ID environment variable not set.")


if __name__ == "__main__":
    main()
