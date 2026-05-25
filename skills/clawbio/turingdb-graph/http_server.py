#!/usr/bin/env python3
"""HTTP endpoint for the turingdb-graph skill.

Thin FastAPI wrapper that calls the same functions as the CLI. Each route
accepts a JSON body with the same parameters as the CLI subcommand, connects
to TuringDB (auto-starting the daemon if unreachable), runs the operation,
and returns the summary dict.

Run locally:
    uvicorn http_server:app --reload

Routes:
    POST /build            {"input_path": ..., "graph": ..., "format": ..., ...}
    POST /query            {"graph": ..., "cypher": ...}
    POST /analyse-cohort   {"graph": ..., "top_n": 10}
    POST /demo             {"which": "cohort" | "pathway" | "antibody"}
    GET  /health           -> {"status": "ok", "host": ...}

Safety note (see SKILL.md § Safety Rules 5): do not expose /query on an
untrusted network without authentication — it executes arbitrary Cypher.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from turingdb_graph import (
    Connection,
    DEFAULT_DATA_DIR,
    DEFAULT_HOST,
    analyse_cohort,
    build_graph,
    run_demo,
    run_query,
)

app = FastAPI(
    title="turingdb-graph",
    version="0.1.0",
    description="HTTP endpoint for the ClawBio turingdb-graph skill.",
)

SKILL_ROOT = Path(__file__).resolve().parent
OUT_ROOT = Path(os.environ.get("TURINGDB_GRAPH_OUT", "/tmp/turingdb-graph-http"))
HOST = os.environ.get("TURINGDB_HOST", DEFAULT_HOST)
DATA_DIR = Path(os.environ.get("TURINGDB_DATA_DIR", str(DEFAULT_DATA_DIR)))
AUTO_START = os.environ.get("TURINGDB_AUTO_START", "1") == "1"


def _connect() -> Connection:
    conn = Connection(host=HOST, data_dir=DATA_DIR)
    try:
        conn.connect(auto_start=AUTO_START)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"TuringDB unreachable: {e}")
    return conn


class BuildRequest(BaseModel):
    input_path: str
    graph: str
    format: str = "auto"
    node_label: str | None = None


class QueryRequest(BaseModel):
    graph: str
    cypher: str
    result_format: str = "md"


class CohortRequest(BaseModel):
    graph: str
    top_n: int = 10


class DemoRequest(BaseModel):
    which: str = "cohort"


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "host": HOST, "data_dir": str(DATA_DIR)}


@app.post("/build")
def http_build(req: BuildRequest) -> dict:
    conn = _connect()
    try:
        return build_graph(
            conn, Path(req.input_path), req.graph,
            fmt=req.format, node_label=req.node_label,
            out_dir=OUT_ROOT / f"build-{req.graph}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/query")
def http_query(req: QueryRequest) -> dict:
    conn = _connect()
    try:
        return run_query(
            conn, req.graph, req.cypher,
            fmt=req.result_format, out_dir=OUT_ROOT / f"query-{req.graph}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyse-cohort")
def http_cohort(req: CohortRequest) -> dict:
    conn = _connect()
    try:
        return analyse_cohort(
            conn, req.graph, top_n=req.top_n,
            out_dir=OUT_ROOT / f"cohort-{req.graph}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/demo")
def http_demo(req: DemoRequest) -> dict:
    conn = _connect()
    try:
        return run_demo(
            conn, req.which, SKILL_ROOT,
            out_dir=OUT_ROOT / f"demo-{req.which}",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
