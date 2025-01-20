import logging
import os
from datetime import datetime
from enum import Enum
from http import HTTPStatus
from typing import Optional, Dict, Any, Generator
from urllib.parse import urlencode

import requests
from IPython import get_ipython
from requests.exceptions import RequestException
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
    retry_if_exception,
)


class AttackIQLogger:
    _instances = {}

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> logging.Logger:
        if name not in cls._instances:
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            logger.propagate = False

            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            if cls.is_jupyter():
                handler = cls.NotebookHandler()
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            cls._instances[name] = logger

        return cls._instances[name]

    @staticmethod
    def is_jupyter():
        try:
            shell = get_ipython().__class__.__name__
            return shell == "ZMQInteractiveShell"
        except NameError:
            return False

    class NotebookHandler(logging.Handler):
        def emit(self, record):
            from IPython.display import display, HTML

            log_entry = self.format(record)
            color = "white"
            if record.levelno >= logging.ERROR:
                color = "red"
            elif record.levelno >= logging.WARNING:
                color = "orange"
            display(HTML(f'<pre style="color: {color}">{log_entry}</pre>'))


logger = AttackIQLogger.get_logger(__name__)


class AttackIQRestClient:
    def __init__(self, platform_url: str, platform_api_token: str):
        self.platform_url = platform_url.rstrip("/")
        self.headers = {
            "Authorization": (
                f"Bearer {platform_api_token}"
                if os.environ.get("IS_AIQ_PLATFORM_ENABLE", "false") == "true"
                else f"Token {platform_api_token}"
            ),
            "Content-Type": "application/json",
        }

    def get_object(
        self, endpoint: str, params: dict = None
    ) -> Optional[Dict[str, Any]]:
        url = self._build_url(endpoint, params)
        logger.info(f"Fetching object from {url}")
        return self._make_request(url, method="get", json=None)

    def get_all_objects(
        self, endpoint: str, params: dict = None
    ) -> Generator[Dict[str, Any], None, None]:
        url = self._build_url(endpoint, params)
        logger.info(f"Fetching objects from {url}")
        total_count = None
        objects_yielded = 0
        while url:
            try:
                data = self._make_request(url, method="get", json=None)
                if not data:
                    break
                results = data.get("results", [])
                if total_count is None:
                    total_count = data.get("count")
                objects_left = total_count - objects_yielded
                logger.info(f"Objects left: {objects_left}")
                for result in results:
                    yield result
                    objects_yielded += 1
                url = data.get("next")
            except RequestException as e:
                logger.error(f"Failed to fetch objects: {e}")
                break

    def get_total_objects_count(
        self, endpoint: str, params: dict = None
    ) -> Optional[int]:
        url = self._build_url(endpoint, params)
        data = self._make_request(url, method="get", json=None)
        return data.get("count") if data else None

    def post_object(self, endpoint: str, data: dict) -> Optional[Dict[str, Any]]:
        url = self._build_url(endpoint)
        logger.info(f"Posting object to {url} with data: {data}")
        return self._make_request(url, method="post", json=data)

    def delete_object(self, endpoint: str) -> Optional[Dict[str, Any]]:
        url = self._build_url(endpoint)
        logger.info(f"Deleting object at {url}")
        return self._make_request(url, method="delete", json=None)

    def _build_url(self, endpoint: str, params: dict = None) -> str:
        if not endpoint.startswith(self.platform_url):
            endpoint = endpoint.lstrip("/")
            url = f"{self.platform_url}/{endpoint}"
        else:
            url = endpoint
        if params:
            url += f"?{urlencode(params)}"
        return url

    @staticmethod
    def _is_retryable_exception(exception):
        if isinstance(exception, RequestException):
            if exception.response is not None:
                return exception.response.status_code in [
                    HTTPStatus.BAD_GATEWAY,
                    HTTPStatus.SERVICE_UNAVAILABLE,
                    HTTPStatus.GATEWAY_TIMEOUT,
                ]
        return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception(_is_retryable_exception),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.DEBUG),
    )
    def _make_request(
        self, url: str, method: str, json: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        try:
            logger.info(f"Request method: {method.upper()} for URL: {url}")
            method = method.lower()
            if method not in ["get", "post", "delete"]:
                raise ValueError(f"Unsupported method: {method}")
            if method == "post" and json:
                logger.info(f"Request data: {json}")
            response = requests.request(method, url, headers=self.headers, json=json)
            if response.status_code == HTTPStatus.NOT_FOUND:
                logger.error(f"Resource not found: {url}")
                return {}
            response.raise_for_status()
            if response.status_code in [
                HTTPStatus.NO_CONTENT,
                HTTPStatus.RESET_CONTENT,
            ]:
                logger.info(
                    f"Request successful: {response.status_code} {response.reason}"
                )
                return {"status_code": response.status_code}
            if response.content:
                return response.json()
            else:
                logger.info(
                    f"Request successful but no content returned: {response.status_code} {response.reason}"
                )
                return {"status_code": response.status_code}
        except requests.RequestException as e:
            if e.response is not None:
                logger.exception(
                    f"_make_request failed method: {method} \n"
                    f"\turl: {url} \n"
                    f"\tstatus: {e.response.status_code} \n"
                    f"\tcontent: {e.response.text} \n"
                    f"\tjson: {json} \n"
                    f"\theaders: {self.headers} \n"
                    f"\texception: {e}"
                )
            else:
                logger.exception(
                    f"_make_request failed method: {method} \n"
                    f"\turl: {url} \n"
                    f"\tjson: {json} \n"
                    f"\theaders: {self.headers} \n"
                    f"\texception: {e}"
                )
            raise e


class ResultsUtils:
    ENDPOINT = "v1/results"

    @staticmethod
    def get_results(
        client: AttackIQRestClient,
        page: int = 1,
        page_size: int = 10,
        search: str = "",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        params = {
            "page": page,
            "page_size": page_size,
            "search": search,
        }
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        yield from client.get_all_objects(ResultsUtils.ENDPOINT, params=params)


class PhaseResultsUtils:
    ENDPOINT = "v1/phase_results"

    @staticmethod
    def get_phase_results(
        client: AttackIQRestClient,
        assessment_id: str,
        project_run_id: Optional[str] = None,
        result_summary_id: Optional[str] = None,
    ) -> Generator[dict, None, None]:
        # BEWARE: created_after is NOT supported by phase_results endpoint yet
        params = {"project_id": assessment_id}
        if project_run_id:
            params["project_run"] = project_run_id
        if result_summary_id:
            params["result_summary"] = result_summary_id
        yield from client.get_all_objects(PhaseResultsUtils.ENDPOINT, params=params)


class PhaseLogsUtils:
    ENDPOINT = "v1/phase_logs"

    @staticmethod
    def get_phase_logs(
        client: AttackIQRestClient,
        scenario_job_id: str,
    ) -> Generator[dict, None, None]:
        # BEWARE: created_after is NOT supported by phase_results endpoint yet
        params = {"scenario_job_id": scenario_job_id}
        yield from client.get_all_objects(PhaseLogsUtils.ENDPOINT, params=params)


class TagSetUtils:
    ENDPOINT = "v1/tag_sets"

    @staticmethod
    def get_tag_set_id(client: AttackIQRestClient, tag_set_name: str) -> Optional[str]:
        logger.info(f"Searching for TagSet: '{tag_set_name}'")
        params = {"name": tag_set_name}
        tag_sets = list(client.get_all_objects(TagSetUtils.ENDPOINT, params=params))
        if tag_sets:
            tag_set = tag_sets[0]
            logger.info(f"TagSet '{tag_set_name}' found with ID '{tag_set['id']}'")
            return tag_set["id"]
        else:
            logger.warning(f"TagSet '{tag_set_name}' not found")
            return None

    @staticmethod
    def get_custom_tag_set_id(client: AttackIQRestClient) -> Optional[str]:
        return TagSetUtils.get_tag_set_id(client, "Custom")


class TagUtils:
    ENDPOINT = "v1/tags"

    @staticmethod
    def get_tags(
        client: AttackIQRestClient, params: dict = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield from client.get_all_objects(TagUtils.ENDPOINT, params=params)

    @staticmethod
    def get_tag_by_id(client: AttackIQRestClient, tag_id: str):
        return client.get_object(f"{TagUtils.ENDPOINT}/{tag_id}")

    @staticmethod
    def create_tag(client: AttackIQRestClient, tag_name: str, tag_set_id: str):
        tag_data = {
            "name": tag_name,
            "display_name": tag_name,
            "tag_set": tag_set_id,
            "meta_data": None,
        }
        logger.info(f"Creating tag '{tag_name}' in tag set ID '{tag_set_id}'")
        return client.post_object(TagUtils.ENDPOINT, data=tag_data)

    @staticmethod
    def get_tag_id(client: AttackIQRestClient, tag_name: str, tag_set_id: str):
        params = {"name": tag_name, "tag_set": tag_set_id}
        if tags := list(client.get_all_objects(TagUtils.ENDPOINT, params=params)):
            tag = tags[0]
            logger.info(f"Tag '{tag_name}' found with ID '{tag['id']}'")
            return tag["id"]
        logger.info(f"Tag '{tag_name}' not found in custom tag set")
        return None

    @staticmethod
    def delete_tag(client: AttackIQRestClient, tag_id: str):
        logger.info(f"Deleting tag with ID '{tag_id}'")
        return client.delete_object(f"{TagUtils.ENDPOINT}/{tag_id}")

    @staticmethod
    def get_or_create_tag(
        client: AttackIQRestClient, tag_name: str, tag_set_name: str
    ) -> str:
        tag_set_id = TagSetUtils.get_tag_set_id(client, tag_set_name)
        if not tag_set_id:
            logger.error(f"Failed to get TagSet ID for '{tag_set_name}'")
            return ""
        tag_id = TagUtils.get_tag_id(client, tag_name, tag_set_id)
        if not tag_id:
            logger.info(f"Tag '{tag_name}' not found. Creating new tag.")
            tag = TagUtils.create_tag(client, tag_name, tag_set_id)
            if not tag:
                logger.error(f"Failed to create tag '{tag_name}'")
                return ""
            tag_id = tag["id"]
        return tag_id

    @staticmethod
    def get_or_create_custom_tag(client: AttackIQRestClient, tag_name: str) -> str:
        return TagUtils.get_or_create_tag(client, tag_name, "Custom")


class TaggedItemUtils:
    ENDPOINT = "v1/tagged_items"

    @staticmethod
    def get_tagged_items(
        client: AttackIQRestClient, content_type: str, object_id: str
    ) -> Generator[Dict[str, Any], None, None]:
        logger.info(
            f"Fetching tagged items for object of type: {content_type} with ID '{object_id}'"
        )
        if content_type not in ["asset", "assessment"]:
            logger.error(
                f"Unsupported content type '{content_type}'. Supported types: 'asset', 'assessment'"
            )
            return
        params = {"content_type": content_type, "object_id": object_id}
        yield from client.get_all_objects(TaggedItemUtils.ENDPOINT, params=params)

    @staticmethod
    def get_tagged_item(
        client: AttackIQRestClient, content_type: str, object_id: str, tag_id: str
    ):
        params = {"content_type": content_type, "object_id": object_id, "tag": tag_id}
        items = list(client.get_all_objects(TaggedItemUtils.ENDPOINT, params=params))
        return items[0] if items else None

    @staticmethod
    def create_tagged_item(
        client: AttackIQRestClient, content_type: str, object_id: str, tag_id: str
    ) -> str:
        logger.info(
            f"Creating tagged item with tag_id '{tag_id}' to object of type: {content_type} with ID '{object_id}'"
        )
        data = {
            "content_type": content_type,
            "object_id": object_id,
            "tag": tag_id,
        }  # tag is the tag_id
        tag_item = client.post_object(TaggedItemUtils.ENDPOINT, data)
        if tag_item:
            tag_item_id = tag_item["id"]
            logger.info(f"Successfully created tagged item with ID {tag_item_id}")
            return tag_item_id
        else:
            logger.error(
                f"Failed to create tag item with tag '{tag_id}' to object with ID '{object_id}'"
            )
            return ""

    @staticmethod
    def delete_tagged_item(client: AttackIQRestClient, tagged_item_id: str) -> bool:
        logger.info(f"Removing tag item with ID {tagged_item_id}")
        response = client.delete_object(f"{TaggedItemUtils.ENDPOINT}/{tagged_item_id}")
        if response:
            logger.info(f"Successfully deleted tag item with ID {tagged_item_id}")
            return True
        else:
            logger.error(f"Failed to delete tagged item with ID {tagged_item_id}")
            return False


class AssetStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class AssetUtils:
    ENDPOINT = "v1/assets"
    ASSET_JOBS_ENDPOINT = "v1/asset_jobs"
    JOB_NAME_DESTROY_SELF = "06230502-890c-4dca-aab1-296706758fd9"

    @staticmethod
    def get_assets(
        client: AttackIQRestClient, params: dict = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield from client.get_all_objects(AssetUtils.ENDPOINT, params=params)

    @staticmethod
    def get_asset_by_id(client: AttackIQRestClient, asset_id: str):
        return client.get_object(f"{AssetUtils.ENDPOINT}/{asset_id}")

    @staticmethod
    def get_asset_by_hostname(
        client: AttackIQRestClient, hostname: str
    ) -> Optional[Dict[str, Any]]:
        params = {"hostname": hostname}
        assets = list(client.get_all_objects(AssetUtils.ENDPOINT, params=params))
        return assets[0] if assets else None

    @staticmethod
    def uninstall_asset(client: AttackIQRestClient, asset_id: str) -> bool:
        logger.info(f"Uninstalling asset with ID: {asset_id}")
        payload = {
            "asset": asset_id,
            "job_name": AssetUtils.JOB_NAME_DESTROY_SELF,
            "one_way": True,
        }
        try:
            response = client.post_object(AssetUtils.ASSET_JOBS_ENDPOINT, data=payload)
            if response:
                logger.info(f"Asset {asset_id} uninstall job submitted successfully")
                return True
            else:
                logger.error(f"Failed to submit uninstall job for asset {asset_id}")
                return False
        except Exception as e:
            logger.error(f"Error while uninstalling asset {asset_id}: {str(e)}")
            return False

    @staticmethod
    def add_tag(client: AttackIQRestClient, asset_id: str, tag_id: str) -> str:
        return TaggedItemUtils.create_tagged_item(client, "asset", asset_id, tag_id)

    @staticmethod
    def get_total_assets(client: AttackIQRestClient) -> Optional[int]:
        logger.info("Fetching total number of assets...")
        return client.get_total_objects_count(AssetUtils.ENDPOINT)

    @staticmethod
    def get_assets_count_by_status(
        client: AttackIQRestClient, status: AssetStatus
    ) -> Optional[int]:
        logger.info(f"Fetching count of assets with status: {status.value}...")
        params = {"status": status.value}
        return client.get_total_objects_count(AssetUtils.ENDPOINT, params=params)


class ConnectorUtils:
    ENDPOINT = "v1/company_connectors"

    @staticmethod
    def get_connectors(
        client: AttackIQRestClient, params: dict = None
    ) -> Generator[Dict[str, Any], None, None]:
        yield from client.get_all_objects(ConnectorUtils.ENDPOINT, params=params)

    @staticmethod
    def get_connector_by_id(client: AttackIQRestClient, connector_id: str):
        return client.get_object(f"{ConnectorUtils.ENDPOINT}/{connector_id}")


class AssessmentUtils:
    ENDPOINT = "v1/assessments"

    @staticmethod
    def run_assessment(client: AttackIQRestClient, assessment_id: str) -> str:
        run_assessment_endpoint = f"{AssessmentUtils.ENDPOINT}/{assessment_id}/run_all"
        run_result = client.post_object(run_assessment_endpoint, data={})
        if not run_result or "run_id" not in run_result:
            raise ValueError("Failed to run the assessment.")

        return run_result["run_id"]

    @staticmethod
    def get_assessment_results(
        client: AttackIQRestClient,
        assessment_id: str,
        run_id: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        params = {"assessment_results": "true", "project_id": assessment_id}
        if run_id:
            params["run_id"] = run_id
        yield from client.get_all_objects("v1/results", params=params)

    @staticmethod
    def get_assessment_by_id(
        client: AttackIQRestClient, assessment_id: str
    ) -> Optional[Dict[str, Any]]:
        return client.get_object(f"{AssessmentUtils.ENDPOINT}/{assessment_id}")

    @staticmethod
    def get_assessments(
        client: AttackIQRestClient,
        params: Optional[Dict[str, Any]] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        yield from client.get_all_objects(AssessmentUtils.ENDPOINT, params=params)

    @staticmethod
    def is_assessment_running(client: AttackIQRestClient, assessment_id: str) -> bool:
        endpoint = f"{AssessmentUtils.ENDPOINT}/{assessment_id}/is_on_demand_running"
        result = client.get_object(endpoint)
        return result.get("message", False) if result else False
