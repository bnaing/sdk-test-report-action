import os
from pathlib import Path
import xml.etree.ElementTree as ET


class ResultCount:
    title = ""
    total = 0
    skipped = 0
    failed = 0
    errors = 0
    successRate = 0

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"{self.title} {self.successRate}% #total={self.total}, skipped={self.skipped}, failed={self.failed}, errors={self.errors}"

    def calculateSuccessRate(self):
        success = self.total - (self.failed + self.errors)
        self.successRate = round(success * 100 / self.total)


class FailedTest:
    errors = []

    def __repr__(self) -> str:
        return ''.join(self.errors)

    def add(self, methodName: str, className: str):
        self.errors.append(f"{methodName} in {className}#")


def parse(path, rc: ResultCount, failed: FailedTest):
    tree = ET.parse(path)
    root = tree.getroot()
    attributes = root.attrib

    countTotal = attributes["tests"]
    countSkipped = attributes["skipped"]
    countFailed = attributes["failures"]
    countError = attributes["errors"]

    rc.total += int(countTotal)
    rc.skipped += int(countSkipped)
    rc.failed += int(countFailed)
    rc.errors += int(countError)

    for element in root:
        if element.tag == "testcase":
            if element.find("failure") != None:
                attrib = element.attrib
                methodName = attrib["name"]
                className = attrib["classname"].split(".")[-1]
                failed.add(methodName, className)


def traverse(repo: ResultCount, uc: ResultCount, failed: FailedTest):
    pathlist = Path().rglob("TEST-*.xml")
    for p in pathlist:
        path = str(p)
        if path.lower().endswith("repositorytest.xml"):
            parse(path, repo, failed)

        elif path.lower().endswith("usecasetest.xml"):
            parse(path, uc, failed)


def main():
    repo = ResultCount("Repository")
    uc = ResultCount("Use Case")
    failed = FailedTest()

    traverse(repo, uc, failed)

    repo.calculateSuccessRate()
    uc.calculateSuccessRate()

    try:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'REPO={repo}', file=fh)
            print(f'USECASE={uc}', file=fh)
            print(f'FAILED={failed}', file=fh)
    except:
        pass


if __name__ == "__main__":
    main()
