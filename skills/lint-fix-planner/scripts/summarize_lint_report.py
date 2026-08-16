#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LINE_RE = re.compile(r"^(?P<path>.+?):(?P<line>\d+):(?:(?P<col>\d+):)?\s*(?P<message>.*)\s\((?P<linter>[^()]+)\)$")

NOISE_PATH_RE = re.compile(
    r"(^|/)(tests?/|internal/docs/|internal/integration/|internal/bench(mark(s)?)?/|.*_example\.go$|.*_test\.go$)"
)
HIGH_RISK_PATH_RE = re.compile(
    r"(^|/)(internal/auth/|internal/service/|internal/repository/|internal/server/|internal/mcp/tools/|internal/mcp/mcpserver/)"
)

AUTO_FIX_LINTERS = {"errcheck", "staticcheck", "unused", "govet"}
LOCAL_REFACTOR_LINTERS = {"funlen", "nestif"}
HIGH_RISK_REFACTOR_LINTERS = {"gocognit", "gocyclo", "cyclop", "dupl"}


def classify_issue(path: str, linter: str, message: str) -> str:
    if NOISE_PATH_RE.search(path):
        if linter in HIGH_RISK_REFACTOR_LINTERS | LOCAL_REFACTOR_LINTERS | AUTO_FIX_LINTERS:
            return "noise_candidate"

    if linter in AUTO_FIX_LINTERS:
        return "auto_fix_candidate"

    if linter in LOCAL_REFACTOR_LINTERS:
        if HIGH_RISK_PATH_RE.search(path):
            return "high_risk_refactor"
        return "local_refactor"

    if linter in HIGH_RISK_REFACTOR_LINTERS:
        if HIGH_RISK_PATH_RE.search(path):
            return "high_risk_refactor"
        return "local_refactor"

    return "unclassified"


def parse_report(report_path: Path) -> dict:
    issues = []
    by_linter = Counter()
    by_path = Counter()
    by_bucket = Counter()
    bucket_examples = defaultdict(list)

    for raw_line in report_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LINE_RE.match(raw_line.strip())
        if not match:
            continue
        item = match.groupdict()
        path = item["path"]
        linter = item["linter"]
        message = item["message"]
        bucket = classify_issue(path, linter, message)

        issue = {
            "path": path,
            "line": int(item["line"]),
            "column": int(item["col"]) if item["col"] else None,
            "linter": linter,
            "message": message,
            "bucket": bucket,
        }
        issues.append(issue)
        by_linter[linter] += 1
        by_path[path] += 1
        by_bucket[bucket] += 1
        if len(bucket_examples[bucket]) < 5:
            bucket_examples[bucket].append(issue)

    return {
        "report_path": str(report_path),
        "total_issues": len(issues),
        "by_linter": dict(by_linter.most_common()),
        "by_path": dict(by_path.most_common()),
        "by_bucket": dict(by_bucket.most_common()),
        "bucket_examples": bucket_examples,
    }


def as_markdown(summary: dict) -> str:
    lines = []
    lines.append(f"Report: `{summary['report_path']}`")
    lines.append(f"Total issues: {summary['total_issues']}")
    lines.append("")
    lines.append("By linter:")
    for linter, count in summary["by_linter"].items():
        lines.append(f"- `{linter}`: {count}")
    lines.append("")
    lines.append("By bucket:")
    for bucket, count in summary["by_bucket"].items():
        lines.append(f"- `{bucket}`: {count}")
    lines.append("")
    lines.append("Top paths:")
    for path, count in list(summary["by_path"].items())[:10]:
        lines.append(f"- `{path}`: {count}")
    lines.append("")
    lines.append("Examples:")
    for bucket, examples in summary["bucket_examples"].items():
        lines.append(f"- `{bucket}`:")
        for issue in examples:
            lines.append(
                f"  - `{issue['path']}:{issue['line']}` `{issue['linter']}` {issue['message']}"
            )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a lint report.")
    parser.add_argument("report_path", help="Path to a text lint report")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    report_path = Path(args.report_path).resolve()
    if not report_path.exists():
        print(f"report not found: {report_path}", file=sys.stderr)
        return 1

    summary = parse_report(report_path)
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(as_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
