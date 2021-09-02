import datetime
import pytz

DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

def parse_motd(input: str) -> dict:
    parts = input.split("<li>")
    output = {}
    for part in parts:
        part = part.replace("</li>", "")
        s = part.split(":")
        if len(s) != 2 and not s[0] == "":
            output["description"] = s[0]
            continue

        if len(s) == 2:
            output[s[0]] = s[1]

    return output


def parse_timestamp(input: str) -> datetime.datetime:
    return datetime.datetime.strptime(input, DATE_FORMAT)

def datetime_to_preferred_tz(input: datetime.datetime, tz: str) -> datetime.datetime:
    if tz == "UTC":
        return input
    utc_tz = pytz.timezone("UTC")
    preferred_tz = pytz.timezone(tz)
    return utc_tz.localize(input).astimezone(preferred_tz)