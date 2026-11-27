"""FastAPI entry point for the public ResearchPilot demo."""

from fastapi import FastAPI

from .demo_selector import run_demo_selection
from .schemas import BandSelectionRequest, BandSelectionResponse


app = FastAPI(
    title="ResearchPilot Public Demo API",
    version="1.0.0",
    description=(
        "Runs public classical band-selection implementations on deterministic "
        "synthetic data. It does not expose research data or experiment results."
    ),
)


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "service": "ResearchPilot", "demo": True}


@app.post("/select-bands", response_model=BandSelectionResponse)
def select_bands_api(request: BandSelectionRequest) -> BandSelectionResponse:
    return run_demo_selection(request)

