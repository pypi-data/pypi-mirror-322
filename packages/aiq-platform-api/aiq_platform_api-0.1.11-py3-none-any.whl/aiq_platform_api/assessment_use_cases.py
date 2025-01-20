# Example notebook: https://colab.research.google.com/drive/1XpDkCMb1myskcQOILK6XaaF1g0a_8666?usp=sharing
import itertools
import os
import time
from typing import Optional

from aiq_platform_api.common_utils import (
    AttackIQRestClient,
    AttackIQLogger,
    AssessmentUtils,
    AssetUtils,
)
from aiq_platform_api.env import ATTACKIQ_API_TOKEN, ATTACKIQ_PLATFORM_URL

logger = AttackIQLogger.get_logger(__name__)


def list_assessments(client: AttackIQRestClient, limit: Optional[int] = None) -> int:
    logger.info(f"Listing assessments (limit: {limit if limit else 'None'})...")
    count = 0
    assessments = AssessmentUtils.get_assessments(client)

    for assessment in itertools.islice(assessments, limit):
        count += 1
        logger.info(f"Assessment {count}:")
        logger.info(f"  ID: {assessment.get('id', 'N/A')}")
        logger.info(f"  Name: {assessment.get('name', 'N/A')}")
        logger.info(f"  Status: {assessment.get('status', 'N/A')}")
        logger.info("---")

    logger.info(f"Total assessments listed: {count}")
    return count


def get_assessment_results(
    client: AttackIQRestClient, assessment_id: str, limit: Optional[int] = None
):
    logger.info(f"Fetching results for assessment ID: {assessment_id}")
    results = AssessmentUtils.get_assessment_results(client, assessment_id)
    for i, result in enumerate(itertools.islice(results, limit)):
        logger.info(f"Result {i}:")
        logger.info(f"  ID: {result.get('id', 'N/A')}")
        logger.info(f"  Status: {result.get('status', 'N/A')}")
        logger.info(f"  Start Time: {result.get('start_time', 'N/A')}")
        logger.info(f"  End Time: {result.get('end_time', 'N/A')}")
        logger.info("---")


def run_assessment(client: AttackIQRestClient, assessment_id: str) -> Optional[str]:
    logger.info(f"Running assessment with ID: {assessment_id}")
    try:
        run_id = AssessmentUtils.run_assessment(client, assessment_id)
        logger.info(f"Assessment started successfully. Run ID: {run_id}")
        return run_id
    except Exception as e:
        logger.error(f"Failed to run assessment: {str(e)}")
        return None


def wait_for_assessment_completion(
    client: AttackIQRestClient,
    assessment_id: str,
    run_id: Optional[str] = None,
    timeout: int = 600,
    check_interval: int = 10,
) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not AssessmentUtils.is_assessment_running(client, assessment_id):
            elapsed_time = round(time.time() - start_time, 2)
            logger.info(
                f"Assessment {assessment_id} (Run ID: {run_id}) completed in {elapsed_time} seconds."
            )
            return True

        if check_interval > 1:
            logger.info(
                f"Assessment {assessment_id} is still running. Waiting {check_interval} seconds..."
            )
        time.sleep(check_interval)

    logger.warning(
        f"Assessment {assessment_id} (Run ID: {run_id}) did not complete within {timeout} seconds."
    )
    return False


def list_assets_in_assessment(
    client: AttackIQRestClient, project_id: str, limit: Optional[int] = None
):
    logger.info(
        f"Listing assets for project ID: {project_id} (limit: {limit if limit else 'None'})..."
    )
    params = {"hide_hosted_agents": "true", "project_id": project_id}
    assets = AssetUtils.get_assets(client, params=params)
    asset_count = 0
    for asset in itertools.islice(assets, limit):
        asset_count += 1
        logger.info(f"Asset {asset_count}:")
        logger.info(f"  ID: {asset.get('id', 'N/A')}")
        logger.info(f"  Name: {asset.get('name', 'N/A')}")
        logger.info(f"  Type: {asset.get('type', 'N/A')}")
        logger.info(f"  IP Address: {asset.get('ipv4_address', 'N/A')}")
        logger.info("---")
    logger.info(f"Total assets listed: {asset_count}")
    return asset_count


def main():
    client = AttackIQRestClient(ATTACKIQ_PLATFORM_URL, ATTACKIQ_API_TOKEN)
    assessment_id = os.environ.get("ATTACKIQ_ASSESSMENT_ID")

    list_assessments(client, limit=5)

    if assessment_id:
        list_assets_in_assessment(client, assessment_id, limit=5)
        get_assessment_results(client, assessment_id, limit=5)
        run_id = run_assessment(client, assessment_id)
        if run_id:
            wait_for_assessment_completion(
                client, assessment_id, run_id, timeout=20, check_interval=1
            )
    else:
        logger.warning(
            "ATTACKIQ_ASSESSMENT_ID environment variable is not set. Skipping assessment-specific operations."
        )


if __name__ == "__main__":
    main()
