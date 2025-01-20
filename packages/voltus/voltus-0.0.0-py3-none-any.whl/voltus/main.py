from io import BytesIO, StringIO
from typing import Any, Dict, List, Optional
# import urllib.parse
import pandas as pd
import requests
# import urllib


class VoltusClient:
    """
    A client for interacting with the Voltus feature store API.

    Attributes:
        api_url (str): The base URL of the Voltus API.
        token (str): The authentication token.
    """

    def __init__(self, api_base_url: str, token: str, verify_requests: bool = True):
        """
        Initializes the VoltusClient.

        Args:
            api_url: The base URL of the Voltus API.
        """

        self.url = (
            api_base_url.replace("\\", "/")
            .replace("https://", "")
            .replace("http://", "")
            .strip("/")
            .strip()
        )
        self.url = api_base_url
        self.token = token
        self.verify_requests = verify_requests
        self.healthcheck()

    def healthcheck(self):
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/current_authenticated_user",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )

        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        response_json = response.json()
        # print(response_json)
        assert (
            response_json["user"]["token"] == self.token
        ), f"Token mismatch: {response.json()}"

    def get_task_status(self, task_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Gets the status of an asynchronous task.

        Args:
            task_id (Optional[str], optional): The ID of the task. If None, retrieves the status of all tasks. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing the status of a task.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/task_status",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={"task_id": task_id},
        )
        return response.json()

    # def get_current_authenticated_user(): TODO

    def add_dataset(
        self,
        dataset: pd.DataFrame,
        dataset_name: str = "new dataset",
        description: str = "",
        overwrite: bool = True,
    ):
        buffer = BytesIO()
        dataset.to_parquet(buffer, index=False)
        buffer.seek(0)
        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/file",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "dataset_name": dataset_name,
                "description": description,
                "overwrite": overwrite,
            },
            files={
                "file": (
                    f"{dataset_name}.parquet",
                    buffer,
                ),
            },
        )
        print(response.text)

    def list_datasets(self) -> List[str]:
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={"detailed": "false"},
        )

        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        return response.json()

    def retrieve_dataset(self, dataset_name: str) -> pd.DataFrame:
        # dataset_name = urllib.parse.quote(dataset_name)
        # print(dataset_name)
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/{dataset_name}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "file_format": "json",
            },
        )
        print(response.text)
        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        return response.json()

    # def delete_datasets(dataset_name: str) -> None: TODO

    # def list_example_datasets() -> List[str]: TODO

    # def retrieve_example_dataset(dataset_name: str) -> pd.DataFrame: TODO

    def apply_feature_function_to_dataset(
        self,
        feature_function_name: str,
        original_datasets: List[str],
        generated_dataset_name: Optional[str] = None,
        generated_dataset_description: Optional[str] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Applies a feature function to existing data.

        Args:
            feature_function_name (str): The name of the feature function to apply.
            original_datasets (List[str]): A list of dataset names to apply the function to
            generated_dataset_name (Optional[str], optional): A name for the generated dataset. Defaults to None.
            generated_dataset_description (Optional[str], optional): A description for the generated dataset. Defaults to None.
            kwargs (Optional[Dict[str, Any]], optional): Keyword arguments for the feature function. Defaults to None.
            overwrite (bool, optional): Whether to overwrite an existing dataset. Defaults to True.

        Returns:
        Dict[str, Any]: A dict with the response message and, if any, task_ids.
        """
        instruction = {
            "feature_function_name": feature_function_name,
            "original_datasets": original_datasets,
            "generated_dataset_name": generated_dataset_name,
            "generated_dataset_description": generated_dataset_description,
            "feature_function_kwargs": kwargs or {},
        }
        params = {"overwrite": overwrite}
        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/apply_to_dataset",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params=params,
            json_data=[instruction],
        )
        return response.json()

    def list_feature_functions(self, detailed: bool = False) -> List[Dict[str, Any]]:
        """
        Lists available feature functions.

        Args:
            detailed (bool, optional): Whether to include detailed information about each feature function. Defaults to False.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a feature function.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={"detailed": detailed},
        )
        return response.json()

    def list_feature_functions_tags(self) -> List[str]:
        """
        Lists all available tags for feature functions.

        Returns:
            List[str]: A list of tags.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/tags",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )
        return response.json()["tags"]

    # def list_trained_models(self) -> List[str]:
    #     """
    #     Lists the available trained ML models.

    #     Returns:
    #         List[str]: A list of model names.
    #     """
    #     response = self._make_request("GET", "/machinelearning/models")
    #     return response.json()


if __name__ == "__main__":
    BASE_URL = "localhost"
    USER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJSaGxFVnUwUUdfQUlZdlo3NlJIc1EtOEQ3Vi11UHJjQkltNk5oeVo1eWhJIn0.eyJleHAiOjE3MzY4OTAwMDksImlhdCI6MTczNjg1NDAwOSwiYXV0aF90aW1lIjoxNzM2ODU0MDA5LCJqdGkiOiIwODBjMDBjMi1kZGRiLTQ1YzYtODFkZS03Zjg2ZWM1MTBiZTQiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L3JlYWxtcy92b2x0dXMiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiZDYzYzUzZmItNWFiMS00YmZmLWIwOWYtZTg3N2Y0MWEyYjVkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoidm9sdHVzIiwic2lkIjoiMWY2ZGYxOWUtYzk5Zi00MjY5LWFlNDUtMGYzZTM3OGJmNjRkIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLXZvbHR1cyIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwgb3BlbmlkIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoidGVzdCB0ZXN0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoidGVzdCIsImdpdmVuX25hbWUiOiJ0ZXN0IiwiZmFtaWx5X25hbWUiOiJ0ZXN0IiwiZW1haWwiOiJ0ZXN0QHRlc3QuY29tIn0.kPzTXTh-48SjV-TXEt4dE9aSYxrWCT_pLS7nd4MLGHoNtllCuGWjADQA1-HcjSPa8CUxXmYw7BCePnmYaD2WfB_dq26BJZPCl7c7WN5nJzkYMHVfHJOAGe-85BqL_3XRCM1vLBuTULY96dwrGezAYEyMWV9dnGBchg2IZK49vxYm8tJSBdAF_GAObhhpsAIRT_QodaNQRa4QHId8IZTSBhmvQ-BqIDlJMRdiHPWeGRhQaBzwo6Lcnl5dyMMxrm6Ynw8LyZQggx2bl70SYiRb190LRFKr-DizqDUazBJsvc5LOektW4leaa-AuO768PNMdAXmMpeuc4lwHAsDojxzhg"

    client = VoltusClient(BASE_URL, USER_TOKEN, verify_requests=False)

    df = pd.read_csv(
        "C:/Users/carlos.t.santos/Desktop/Files/Reps/feature-store/clients/python-client/python_client/energy_data.csv"
    )
    client.add_dataset(df)

    dataset_names = client.list_datasets()
    for dataset_name in dataset_names:
        print(dataset_name)

    client.retrieve_dataset(dataset_names[0])
