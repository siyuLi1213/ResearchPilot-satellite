import json
import re
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = PROJECT_ROOT / "workflow" / "ResearchPilot-Public.yml"


def load_workflow():
    with WORKFLOW_PATH.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def test_examples_are_valid_json():
    for path in sorted((PROJECT_ROOT / "examples").glob("*.json")):
        with path.open(encoding="utf-8") as stream:
            json.load(stream)


def test_workflow_graph_is_complete():
    workflow = load_workflow()
    graph = workflow["workflow"]["graph"]
    nodes = graph["nodes"]
    edges = graph["edges"]
    node_ids = {node["id"] for node in nodes}

    assert len(nodes) == 10
    assert len(edges) == 9
    assert all(edge["source"] in node_ids for edge in edges)
    assert all(edge["target"] in node_ids for edge in edges)

    classifier = next(
        node for node in nodes if node["data"]["type"] == "question-classifier"
    )
    class_ids = {str(item["id"]) for item in classifier["data"]["classes"]}
    branch_handles = {
        str(edge["sourceHandle"])
        for edge in edges
        if edge["source"] == classifier["id"]
    }
    assert class_ids == branch_handles


def test_public_bindings_and_fixed_fisher_request():
    nodes = load_workflow()["workflow"]["graph"]["nodes"]
    retrieval = next(
        node for node in nodes if node["data"]["type"] == "knowledge-retrieval"
    )
    http = next(node for node in nodes if node["data"]["type"] == "http-request")

    assert retrieval["data"]["dataset_ids"] == [
        "REBIND_KNOWLEDGE_BASE_AFTER_IMPORT"
    ]
    assert http["data"]["url"] == (
        "https://researchpilot-api.example.invalid/select-bands"
    )
    body = json.loads(http["data"]["body"]["data"][0]["value"])
    assert body == {"dataset": "PaviaU", "method": "fisher", "k": 10}


def test_public_files_have_no_high_signal_secret_or_local_path():
    files = [
        path
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file() and "tests" not in path.parts
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)

    assert not re.search(r"[A-Za-z]:\\", text)
    assert "host" + ".docker.internal" not in text
    assert "127" + ".0.0.1" not in text
    assert not re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", text)
    assert not re.search(r"AKIA[0-9A-Z]{16}", text)
    assert not re.search(r"gh[pousr]_[A-Za-z0-9_]{20,}", text)
    assert not re.search(r"sk-[A-Za-z0-9_-]{20,}", text)

