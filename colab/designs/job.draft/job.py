"""Proposed 05.NN batch writer. Creates requests; never executes their commands."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PAGE = re.compile(r"^(\d{4})\.(.+)$")
BATCH = re.compile(r"^05\.(\d{2})\.md$")


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise Invalid(f"Cannot read JSON {path}: {exc}") from exc


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"Missing text: {label}")
    require("\x00" not in value, f"NUL in {label}")
    return value.strip()


def line(value, label):
    value = text(value, label)
    require("\n" not in value and "\r" not in value, f"{label} must be one line")
    return value


def local(root, value, label, exists=True):
    value = text(value, label)
    rel = Path(value)
    require(not rel.is_absolute() and not rel.drive and ".." not in rel.parts,
            f"{label} must be a project-relative path without '..'")
    path = (root / rel).resolve()
    require(path.is_relative_to(root), f"{label} leaves project (including symlink/junction)")
    if exists:
        require(path.exists(), f"Missing {label}: {value}; name an existing source, do not invent it")
    return path


def resolve_route(root, context, policy):
    require(policy.get("status") == "proposal", "Routing policy must declare status: proposal")
    require(isinstance(policy.get("routes"), list), "Policy needs routes[]")
    context = context.resolve()
    require(context.exists() and context.is_relative_to(root), "Context must exist inside project")
    directory = context if context.is_dir() else context.parent
    # Explicit routing, not 00.live: that file currently selects a law book.
    matches = []
    for route in policy["routes"]:
        require(isinstance(route, dict), "Each route must be an object")
        book = local(root, route.get("book"), "route book")
        if directory == book or directory.is_relative_to(book):
            matches.append((route, book))
    require(len(matches) == 1,
            "Context needs exactly one explicit book route. Add/correct policy routes; no guessed destination")
    route, book = matches[0]
    require(book.is_dir() and (book / "00.md").is_file(), "Routed book needs its existing 00.md sentinel")
    name = line(route.get("jobs_page"), "route jobs_page")
    match = PAGE.fullmatch(name)
    require(match and Path(name).name == name and not name.endswith((".reserved", ".09")),
            "jobs_page must be an existing PPPP.title work page, not reserved or retired")
    low = route.get("work_min")
    high = route.get("work_max")
    require(type(low) is int and type(high) is int and 0 <= low <= high <= 9999,
            "Route must explicitly declare work_min/work_max (proposal; not automatic band law)")
    require(low <= int(match[1]) <= high, "Job page lies outside declared work range")
    page = local(root, (book.relative_to(root) / name).as_posix(), "jobs page")
    require(page.is_dir(), "jobs_page must be a directory; prototype does not allocate pages")
    require(not any(p.name.endswith(".reserved") for p in page.relative_to(root).parents),
            "Reserved ancestor is not an output location")
    allocation = line(route.get("routing_basis"), "route routing_basis")
    return book, page, match[1], match[2], allocation


def validate(root, request, contracts):
    require(isinstance(request, dict), "Request must be an object")
    for key in ("who", "why", "overview"):
        text(request.get(key), key)
    line(request["who"], "who")
    cite = line(request.get("cite"), "cite")
    require(re.fullmatch(r"[1-9](?:\.[1-9]){0,2}(?:,[1-9](?:\.[1-9]){0,2})*", cite),
            "cite must be an intent key of 1–3 axioms per piece; never permission")
    items = request.get("items")
    require(isinstance(items, list) and 1 <= len(items) <= 99, "items must hold 1–99 requests")
    ids = [item.get("id") if isinstance(item, dict) else None for item in items]
    require(all(type(i) is int and 1 <= i <= 99 for i in ids) and len(set(ids)) == len(ids),
            "Item ids must be distinct integers 1–99; these are markers, not task/ticket slot allocations")
    graph = {}
    for item in items:
        label = f"#{item['id']:02}"
        for key in ("title", "issue", "recommend", "ask", "done"):
            text(item.get(key), f"{label} {key}")
        line(item["title"], f"{label} title")
        command = item.get("command")
        require(command in contracts["commands"], f"{label}: unknown command {command!r}; describe known commands first")
        require(type(item.get("scale")) is int and 1 <= item["scale"] <= 5, f"{label}: scale must be 1–5")
        local(root, item.get("target"), f"{label} target")
        sources = item.get("sources")
        require(isinstance(sources, list) and sources, f"{label}: needs source paths and exact sections")
        for src in sources:
            require(isinstance(src, dict), f"{label}: source must be an object")
            path = local(root, src.get("path"), f"{label} source")
            require(path.is_file(), f"{label}: source must be a file")
            section = line(src.get("section"), f"{label} source section")
            headings = re.findall(r"^#{1,6}\s+(.+?)\s*$", path.read_text(encoding="utf-8-sig"), re.M)
            require(section in headings, f"{label}: section {section!r} absent from {src['path']}")
        params = item.get("parameters", {})
        require(isinstance(params, dict), f"{label}: parameters must be an object")
        for field in contracts["commands"][command]["requires"]:
            text(params.get(field), f"{label} {command}.{field}")
        deps = item.get("depends_on", [])
        require(isinstance(deps, list) and all(type(d) is int and d in ids and d != item["id"] for d in deps),
                f"{label}: dependencies must name other items in this batch")
        require(len(deps) == len(set(deps)), f"{label}: duplicate dependency")
        graph[item["id"]] = deps
    visiting, visited = set(), set()
    def visit(number):
        require(number not in visiting, "Dependency cycle; split or correct coupled requests")
        if number in visited:
            return
        visiting.add(number)
        for dep in graph[number]:
            visit(dep)
        visiting.remove(number)
        visited.add(number)
    for number in graph:
        visit(number)
    # Dependency before dependent; severity and id are stable tie-breaks only.
    ordered = []
    pending = list(items)
    while pending:
        ready = [i for i in pending if all(d in {x['id'] for x in ordered} for d in graph[i['id']])]
        item = min(ready, key=lambda i: (i["scale"], i["id"]))
        ordered.append(item)
        pending.remove(item)
    return ordered


def field(name, value):
    # Content cannot introduce a top-level #NN, Ask, or reply by a newline.
    rows = str(value).splitlines()
    return f"{name}: {rows[0]}\n" + "".join(f"    {row}\n" for row in rows[1:])


def render(root, book, page, number, keyword, basis, slot, request, items, contracts):
    parents = book.relative_to(root).parts
    out = [f"# 05.{slot:02}\n\nAuthorization: draft — {date.today().isoformat()}\n",
           field("who", request["who"]), "state: open\nFace: 05\n",
           field("PPPP", number), field("book", book.name), field("keyword", keyword),
           field("location", page.relative_to(root).as_posix()), field("why", request["why"]),
           field("cite", request["cite"]), "\n",
           field("Overview", request["overview"]),
           field("Routing basis", basis),
           f"Contract: proposal revision {contracts['revision']}; not governing law.\n",
           "How: Requests only. Blank reply does not release work. A filled reply still requires the governing behavior and scope check.\n",
           "Scale: 1 walk halts; 2 competing lawful lines; 3 careful sitting survives; 4 wording; 5 no break.\n"]
    # These labels report physical placement, not address.proof or ownership.
    if len(parents) >= 3:
        out[6:6] = [field("desk", parents[-3]), field("shelf", parents[-2])]
    for item in items:
        contract = contracts["commands"][item["command"]]
        out.extend([f"\n#%02d %s\n\n" % (item["id"], item["title"]),
                    field("issue", item["issue"]), field("recommend", item["recommend"]),
                    field("Ask", f">{item['command']} {item['ask']}"),
                    field("path", item["target"]), field("scale", item["scale"]),
                    field("purpose", contract["purpose"]),
                    field("depends_on", ", ".join(f"#{d:02}" for d in item.get("depends_on", [])) or "none")])
        for src in item["sources"]:
            out.append(field("source", f"{src['path']} — section: {src['section']}"))
        for key in contract["requires"]:
            out.append(field(key, item["parameters"][key]))
        out.extend([field("done", item["done"]), field("hold", contract["hold"]),
                    "\nreply:\n\nreceipt: pending; not executed\n"])
    return "".join(out)


def create(root, context, policy, request, contracts, write=False):
    root = root.resolve()
    require(root.is_dir(), "Project root must exist")
    require(contracts.get("status") == "proposal", "Contracts must declare proposal status")
    items = validate(root, request, contracts)
    book, page, number, keyword, basis = resolve_route(root, context, policy)
    seen = []
    for path in page.iterdir():
        match = BATCH.fullmatch(path.name)
        if match:
            seen.append(int(match[1]))
    slot = max(seen, default=0) + 1
    require(slot <= 99, "05.NN range exhausted. Preserve batches; ask Director for a new location. No wrap/reuse")
    while slot <= 99:
        target = page / f"05.{slot:02}.md"
        body = render(root, book, page, number, keyword, basis, slot, request, items, contracts)
        if not write:
            return target, body
        try:
            # Exclusive create protects against another worker choosing the same NN.
            with target.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(body)
            return target, body
        except FileExistsError:
            slot += 1
    raise Invalid("Concurrent writers exhausted remaining slots; no file overwritten")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["describe", "prepare"])
    parser.add_argument("--command")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--contracts", type=Path, default=HERE / "commands.json")
    parser.add_argument("--write", action="store_true", help="Create batch; default is preview")
    args = parser.parse_args()
    try:
        contracts = read_json(args.contracts)
        if args.operation == "describe":
            value = contracts["commands"].get(args.command) if args.command else contracts
            require(value is not None, "Unknown command; run describe without --command")
            print(json.dumps(value, indent=2, ensure_ascii=False))
            return 0
        require(all((args.project, args.context, args.policy, args.request)),
                "prepare needs --project, --context, --policy, --request")
        target, body = create(args.project, args.context, read_json(args.policy),
                              read_json(args.request), contracts, args.write)
        print(f"{'CREATED' if args.write else 'PREVIEW'}: {target}\n\n{body}")
        return 0
    except (Invalid, OSError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
