from pathlib import Path
import xml.etree.ElementTree as ET


class ResultCount:
    title = ""
    total = 0
    skipped = 0
    failed = 0
    errors = 0

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"{self.title} - total={self.total}, skipped={self.skipped}, failed={self.failed}, errors={self.errors}"


class FailedTest:
    methodName = ""
    className = ""

    def __init__(self, methodName: str, className: str) -> None:
        self.methodName = methodName
        self.className = className

    def __repr__(self) -> str:
        return f"`{self.methodName}` in {self.className}"


def parse(path, rc: ResultCount) -> FailedTest:
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
                return FailedTest(methodName, className)


def traverse(repo: ResultCount, uc: ResultCount):
    failedTests = []

    pathlist = Path().rglob("TEST-*.xml")
    for p in pathlist:
        path = str(p)
        if path.lower().endswith("repositorytest.xml"):
            ft = parse(path, repo)
            if ft != None:
                failedTests.append(ft)

        elif path.lower().endswith("usecasetest.xml"):
            ft = parse(path, uc)
            if ft != None:
                failedTests.append(ft)

    return failedTests


def main():
    repo = ResultCount("Repository")
    uc = ResultCount("Use Case")

    failedTests = traverse(repo, uc)

    print(repo)
    print(uc)
    print(failedTests)


if __name__ == "__main__":
    main()
