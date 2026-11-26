"""Request and response models for the public demo API."""

from typing import Literal

from pydantic import BaseModel, Field


BandSelectionMethod = Literal["fisher", "mrmr", "mvpca", "ie", "random", "uniform"]


class BandSelectionRequest(BaseModel):
    dataset: Literal["PaviaU"] = "PaviaU"
    method: BandSelectionMethod = "fisher"
    k: int = Field(ge=1, le=103)


class BandSelectionResponse(BaseModel):
    status: Literal["success"] = "success"
    demo: Literal[True] = True
    dataset: Literal["PaviaU"] = "PaviaU"
    data_source: Literal["synthetic"] = "synthetic"
    method: BandSelectionMethod
    k: int
    selected_bands: list[int]
    index_base: Literal[0] = 0
    band_count: Literal[103] = 103
    note: str

