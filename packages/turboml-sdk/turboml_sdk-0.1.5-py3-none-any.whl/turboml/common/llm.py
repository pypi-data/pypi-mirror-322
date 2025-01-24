import logging
import time

from turboml.common.types import GGUFModelId
from .api import api
from .models import (
    LlamaServerRequest,
    LlamaServerResponse,
    HFToGGUFRequest,
    ModelAcquisitionJob,
)

logger = logging.getLogger("turboml.llm")


def acquire_hf_model_as_gguf(
    hf_repo_id: str,
    model_type: HFToGGUFRequest.GGUFType = HFToGGUFRequest.GGUFType.AUTO,
    select_gguf_file: str | None = None,
) -> GGUFModelId:
    """
    Attempts to acquires a model from the Hugging Face repository and convert
    it to the GGUF format. The model is then stored in the TurboML system, and
    the model key is returned.
    """
    req = HFToGGUFRequest(
        hf_repo_id=hf_repo_id,
        model_type=model_type,
        select_gguf_file=select_gguf_file,
    )
    acq_resp = api.post("acquire_hf_model_as_gguf", json=req.model_dump()).json()
    status_endpoint = acq_resp["status_endpoint"]
    last_status = None
    last_progress = None

    while True:
        job_info = api.get(status_endpoint.lstrip("/")).json()
        job_info = ModelAcquisitionJob(**job_info)

        status = job_info.status
        progress = job_info.progress_message or "No progress info"

        if status != last_status or progress != last_progress:
            logger.info(f"[hf-acquisition] Status: {status}, Progress: {progress}")
            last_status = status
            last_progress = progress

        if status == "completed":
            gguf_id = job_info.gguf_id
            if not gguf_id:
                raise AssertionError("GGUF ID not found in job_info")
            logger.info(f"[hf-acquisition] Acquisition Done, gguf_id = {gguf_id}")
            return GGUFModelId(gguf_id)
        elif status == "failed":
            error_msg = job_info.error_message or "Unknown error"
            raise RuntimeError(f"HF->GGUF acquisition failed: {error_msg}")

        time.sleep(5)


def spawn_llm_server(req: LlamaServerRequest) -> LlamaServerResponse:
    """
    If source_type=HUGGINGFACE, we do the async acquisition under the hood,
    but we poll until it’s done. Then we do the normal /model/openai call.
    """
    if req.source_type == LlamaServerRequest.SourceType.HUGGINGFACE:
        if not req.hf_spec:
            raise ValueError("hf_spec is required for source_type=HUGGINGFACE")
        gguf_id = acquire_hf_model_as_gguf(
            hf_repo_id=req.hf_spec.hf_repo_id,
            model_type=req.hf_spec.model_type,
            select_gguf_file=req.hf_spec.select_gguf_file,
        )
        req.source_type = LlamaServerRequest.SourceType.GGUF_ID
        req.gguf_id = gguf_id

    resp = api.post("model/openai", json=req.model_dump())
    return LlamaServerResponse(**resp.json())


def stop_llm_server(server_id: str):
    """
    To DE_acquire(iLETE /model/openai/{server_id}
    """
    api.delete(f"model/openai/{server_id}")
