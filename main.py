import json
from platform import python_version
from sys import stderr
from time import sleep
from traceback import format_exc
from argparse import ArgumentParser
import requests
from prometheus_client import start_http_server, Gauge

TABLE_ID = "tblFkqWvQKUIXYjMK"
AIRTABLE_APP_ID = "apppg7RHZv6feM66l"
AIRTABLE_URL = (
    f"https://airtable.com/v0.3/application/{AIRTABLE_APP_ID}/readForSharedPages"
)


class Fields:
    EVENT_NAME = "fld1JdoFOTTTo3RvE"
    SIGNUP_COUNT = "fldlYIqhEy8Urh3MA"


class EventData:
    def __init__(self, id, name, signups):
        self.id = id
        self.name = name
        self.signups = signups


def get_leaderboard_data(print_data: bool = False) -> list[EventData]:
    headers = {
        "User-Agent": f"Daydream Watcher (https://github.com/MMK21Hub/daydream-watcher) Python/{python_version()}",
        "Accept": "application/json",
        "x-time-zone": "Europe/London",
        "x-airtable-application-id": AIRTABLE_APP_ID,
        "X-Requested-With": "XMLHttpRequest",
    }

    params = {
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

    response = requests.get(AIRTABLE_URL, headers=headers, params=params)
    if print_data:
        print(response)
        print(response.text)
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
    parser = ArgumentParser()
    parser.add_argument(
        "--port",
        type=int,
        default=9020,
        help="the port to run the Prometheus exporter on",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="log whenever data is scraped (use -vv to print the whole response)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="how often to fetch data from Airtable, in seconds",
    )
    args = parser.parse_args()

    start_http_server(args.port)
    print(f"Started metrics exporter: http://localhost:{args.port}/metrics", flush=True)

    has_had_success = False
    signups_gauge = Gauge(
        "daydream_signups", "Number of signups per event", ["event_name", "event_id"]
    )

    while True:
        try:
            leaderboard = get_leaderboard_data(print_data=args.verbose >= 2)
            has_had_success = True
            if args.verbose:
                print(f"Successfully fetched data for {len(leaderboard)} events")
            for event in leaderboard:
                signups_gauge.labels(event.name, event.id).set(event.signups)
        except Exception as e:
            # Exit the program if the first fetch fails
            if not has_had_success:
                raise e
            print(f"Failed to fetch data: {format_exc()}", file=stderr, flush=True)
        finally:
            sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
