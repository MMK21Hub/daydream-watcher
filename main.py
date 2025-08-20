import requests


class EventData:
    def __init__(self, index, name, signups):
        self.index = index
        self.name = name
        self.signups = signups


def get_leaderboard_data() -> list[EventData]:
    URL = "https://airtable.com/v0.3/application/apppg7RHZv6feM66l/readForSharedPages?stringifiedObjectParams=%7B%22includeDataForPageId%22%3A%22pagR7WnlKBl0YfLVQ%22%2C%22shouldIncludeSchemaChecksum%22%3Atrue%2C%22expectedPageLayoutSchemaVersion%22%3A26%2C%22shouldPreloadQueries%22%3Atrue%2C%22shouldPreloadAllPossibleContainerElementQueries%22%3Atrue%2C%22urlSearch%22%3A%22%22%2C%22includeDataForExpandedRowPageFromQueryContainer%22%3Atrue%2C%22includeDataForAllReferencedExpandedRowPagesInLayout%22%3Atrue%2C%22navigationMode%22%3A%22view%22%7D&requestId=reqOQaQGDTDWbaKRI&accessPolicy=%7B%22allowedActions%22%3A%5B%7B%22modelClassName%22%3A%22page%22%2C%22modelIdSelector%22%3A%22pagR7WnlKBl0YfLVQ%22%2C%22action%22%3A%22read%22%7D%2C%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22apppg7RHZv6feM66l%22%2C%22action%22%3A%22readForSharedPages%22%7D%2C%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22apppg7RHZv6feM66l%22%2C%22action%22%3A%22readSignedAttachmentUrls%22%7D%2C%7B%22modelClassName%22%3A%22application%22%2C%22modelIdSelector%22%3A%22apppg7RHZv6feM66l%22%2C%22action%22%3A%22readInitialDataForBlockInstallations%22%7D%5D%2C%22shareId%22%3A%22shrWJQJs5YsqWocLz%22%2C%22applicationId%22%3A%22apppg7RHZv6feM66l%22%2C%22generationNumber%22%3A0%2C%22expires%22%3A%222025-09-11T00%3A00%3A00.000Z%22%2C%22signature%22%3A%22fbd503372b322e269d96135020d7da5e11a61925589c5a36cab8d6b6e23130a2%22%7D"
    TABLE_ID = "tblFkqWvQKUIXYjMK"

    class Fields:
        EVENT_NAME = "fld1JdoFOTTTo3RvE"
        SIGNUP_COUNT = "fldlYIqhEy8Urh3MA"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "x-time-zone": "Europe/London",
        "x-user-locale": "en",
        "x-airtable-client-queue-time": "0",
        "x-airtable-application-id": "apppg7RHZv6feM66l",
        "x-airtable-page-load-id": "pglA85iQJNGw1Y8U8",
        "x-airtable-inter-service-client": "webClient",
        "x-airtable-inter-service-client-code-version": "b1103f19d1076e5968d3d9645456bc3fb761658b",
        "traceparent": "00-7766e0a6e355f528cb4d0c08590a5647-9aa0fbf10d2f99bc-01",
        "tracestate": "",
        "X-Requested-With": "XMLHttpRequest",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    response = requests.get(URL, headers=headers)
    data = response.json()
    rows = data["data"]["preloadPageQueryResults"]["tableDataById"][TABLE_ID][
        "partialRowById"
    ]
    events = []
    for row_id, row in rows.items():
        cells = row["cellValuesByColumnId"]
        city = cells.get(Fields.EVENT_NAME)
        signup_count = cells.get(Fields.SIGNUP_COUNT)
        events.append(EventData(row_id, city, signup_count))
    return events


def main():
    leaderboard = get_leaderboard_data()
    for event in leaderboard:
        print(f"{event.name}       {event.signups}")


if __name__ == "__main__":
    main()
