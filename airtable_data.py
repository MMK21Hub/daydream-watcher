import json


TABLE_ID = "tblFkqWvQKUIXYjMK"
AIRTABLE_APP_ID = "apppg7RHZv6feM66l"
AIRTABLE_URL = (
    f"https://airtable.com/v0.3/application/{AIRTABLE_APP_ID}/readForSharedPages"
)

AIRTABLE_REQUEST_PARAMS = params = {
    "stringifiedObjectParams": json.dumps(
        {
            "includeDataForPageId": "pagR7WnlKBl0YfLVQ",
            "expectedPageLayoutSchemaVersion": 26,
            "shouldPreloadQueries": True,
            "shouldPreloadAllPossibleContainerElementQueries": True,
            "urlSearch": "",
            "includeDataForExpandedRowPageFromQueryContainer": True,
            "includeDataForAllReferencedExpandedRowPagesInLayout": True,
            "navigationMode": "view",
        }
    ),
    "requestId": "reqOQaQGDTDWbaKRI",
    "accessPolicy": json.dumps(
        {
            "allowedActions": [
                {
                    "modelClassName": "page",
                    "modelIdSelector": "pagR7WnlKBl0YfLVQ",
                    "action": "read",
                },
                {
                    "modelClassName": "application",
                    "modelIdSelector": AIRTABLE_APP_ID,
                    "action": "readForSharedPages",
                },
                {
                    "modelClassName": "application",
                    "modelIdSelector": AIRTABLE_APP_ID,
                    "action": "readSignedAttachmentUrls",
                },
                {
                    "modelClassName": "application",
                    "modelIdSelector": AIRTABLE_APP_ID,
                    "action": "readInitialDataForBlockInstallations",
                },
            ],
            "shareId": "shrWJQJs5YsqWocLz",
            "applicationId": AIRTABLE_APP_ID,
            "generationNumber": 0,
            "expires": "2025-09-11T00:00:00.000Z",
            "signature": "fbd503372b322e269d96135020d7da5e11a61925589c5a36cab8d6b6e23130a2",
        }
    ),
}


class Fields:
    EVENT_NAME = "fld1JdoFOTTTo3RvE"
    SIGNUP_COUNT = "fldlYIqhEy8Urh3MA"
