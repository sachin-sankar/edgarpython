from typing import List

from requests import get

from edgarpy.exceptions import InvalidCIK
from edgarpy.models import Submission

API_BASE = "https://data.sec.gov"
USERAGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
HEADERS = {"User-Agent": USERAGENT}


def getSubmissionsByCik(cik: str) -> List[Submission]:
    reqUrl = API_BASE + f"/submissions/CIK{cik}.json"
    print(reqUrl)
    resp = get(reqUrl, timeout=5000, headers=HEADERS)
    match resp.status_code:
        case 404:
            raise InvalidCIK
        case 200:
            pass
        case _:
            raise RuntimeError(
                f"SECAPI call failed with status code {resp.status_code}"
            )
    data = resp.json()
    data = data["filings"]["recent"]
    submissions = []
    for subZiped in zip(data["form"], data["accessionNumber"]):
        submissions.append(Submission(form=subZiped[0], accessionNumber=subZiped[1]))
    return submissions
