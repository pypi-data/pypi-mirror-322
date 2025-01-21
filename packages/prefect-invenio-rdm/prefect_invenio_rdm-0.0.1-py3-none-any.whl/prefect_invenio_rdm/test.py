# pylint: disable-all
from urllib.parse import quote_plus
import asyncio
from prefect import flow
from prefect_invenio_rdm.flows import create_record_dir
from prefect_invenio_rdm.models.records import DraftConfig, Access
from prefect_invenio_rdm.credentials import InvenioRDMCredentials
from prefect_invenio_rdm.models.api import APIResult
import requests


@flow
def test_upload() -> None:
    base_url = "https://sandbox.zenodo.org/api"
    token = "wKs4iw2SR5n5ZCcKR8mI0fGRQczCWefwZPEO1m09sCjsI1fxIzhwZWJuFDIo"
    headers = {"Authorization": f"Bearer {token}"}
    result = requests.post(
        url=f"{base_url}/records",
        headers=headers,
        json={
            "access": {"record": "public", "files": "public"},
            "files": {"enabled": True},
            "metadata": {
                "creators": [
                    {
                        "person_or_org": {
                            "family_name": "Brown",
                            "given_name": "Troy",
                            "type": "personal",
                        }
                    },
                    {
                        "person_or_org": {
                            "family_name": "Collins",
                            "given_name": "Thomas",
                            "identifiers": [
                                {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                            ],
                            "name": "Collins, Thomas",
                            "type": "personal",
                        },
                        "affiliations": [{"id": "01ggx4157", "name": "Entity One"}],
                    },
                ],
                "publication_date": "2020-06-01",
                "resource_type": {"id": "image-photo"},
                "title": "A Romans story",
            },
        },
    )

    print(result.json())

    id = result.json()["id"]

    print(id)

    result = requests.post(
        url=f"{base_url}/records/{id}/draft/files",
        headers=headers,
        json=[{"key": "ESID_001.zip"}],
    )

    print(result.json())

    with open("/home/joel/Desktop/zenodo/test/ESID_001.zip", "rb") as fp:
        response = requests.put(
            url=f"{base_url}/records/{id}/draft/files/ESID_001.zip/content",
            headers=headers,
            data=fp,
        )
        print(response.json())

    response = requests.post(
        f"{base_url}/records/{id}/draft/files/ESID_001.zip/commit", headers=headers
    )

    print(response.json())


@flow(log_prints=True)
async def upload_data() -> None:
    # create credentials
    credentials = InvenioRDMCredentials(
        base_url="https://sandbox.zenodo.org/api/",
        token="wKs4iw2SR5n5ZCcKR8mI0fGRQczCWefwZPEO1m09sCjsI1fxIzhwZWJuFDIo",
    )

    # provide draft record configurations
    config = DraftConfig(
        record_access=Access.PUBLIC,
        files_access=Access.PUBLIC,
        files_enabled=True,
        metadata={
            "creators": [
                {
                    "person_or_org": {
                        "family_name": "Collins",
                        "given_name": "Thomas",
                        "identifiers": [
                            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
                        ],
                        "name": "Collins, Thomas",
                        "type": "personal",
                    },
                    "affiliations": [{"id": "01ggx4157", "name": "Entity One"}],
                },
            ],
            "publisher": "InvenioRDM",
            "publication_date": "2025-01-10",
            "resource_type": {"id": "dataset"},
            "title": "My dataset",
        },
        community_id="9d50c9c1-afd0-4dc1-ad50-91040788af4f",
        custom_fields={
            "code:codeRepository": "https://github.com/organization/repository",
            "code:developmentStatus": {"id": "wip"},
            "code:programmingLanguage": [{"id": "python"}],
        },
    )

    # upload data from a directory
    result: APIResult = await create_record_dir(
        credentials=credentials,
        directory="/home/joel/Desktop/zenodo/test",
        config=config,
        file_pattern="*.zip",
        delete_on_failure=True,
        auto_publish=False,
    )
    print(result)


if __name__ == "__main__":
    # asyncio.run(test_upload())
    test_upload()
