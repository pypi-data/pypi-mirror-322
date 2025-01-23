import asyncio
import json
import traceback
from typing import Iterable

import aiohttp
import requests

from maitai._config import config
from maitai._maitai_client import MaitaiClient
from maitai._types import EvaluateCallback
from maitai._utils import __version__ as version
from maitai._utils import chat_completion_chunk_to_response
from maitai.models.chat import (
    ChatCompletionChunk,
    ChatCompletionParams,
    ChatCompletionResponse,
    EvaluateRequest,
    EvaluateResponse,
    EvaluationContentType,
)
from maitai.models.metric import RequestTimingMetric


def _get_content_type(content, partial=None):
    if partial is not None:
        return EvaluationContentType.PARTIAL
    if isinstance(content, str):
        return EvaluationContentType.TEXT
    elif isinstance(content, list):
        return EvaluationContentType.MESSAGE


class Evaluator(MaitaiClient):

    def __init__(self):
        super().__init__()

    @classmethod
    async def evaluate_async(
        cls,
        session_id,
        reference_id,
        intent,
        content,
        content_type=None,
        application_id=None,
        application_ref_name=None,
        callback=None,
        completion_params: dict = None,
        chat_completion_response: ChatCompletionResponse = None,
        chat_completion_chunk: ChatCompletionChunk = None,
        timing: RequestTimingMetric = None,
        metadata: dict = {},
    ):
        if content_type is None:
            content_type = _get_content_type(content)
        if content_type is None:
            raise Exception("Unable to automatically determine content_type")
        if application_id is None and application_ref_name is None:
            raise Exception("application_id or application_ref_name must be provided")
        eval_request = cls.create_eval_request(
            application_id,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
        )
        if completion_params is not None:
            eval_request["chat_completion_request"] = {
                "application_ref_name": application_ref_name,
                "session_id": session_id,
                "reference_id": reference_id,
                "action_type": intent,
                "apply_corrections": False,
                "evaluation_enabled": True,
                "params": completion_params,
                "return_evaluation": True if callback else False,
                "auth_keys": config.auth_keys.model_dump(),
                "metadata": metadata,
            }
            if chat_completion_chunk is not None:
                chat_completion_response = chat_completion_chunk_to_response(
                    chat_completion_chunk, content
                )
            eval_request["chat_completion_response"] = (
                chat_completion_response.model_dump()
                if chat_completion_response
                else None
            )
        eval_request["timing_metrics"] = timing.model_dump() if timing else None
        await asyncio.create_task(
            cls.send_evaluation_request_async(eval_request, callback)
        )

    @classmethod
    def evaluate(
        cls,
        session_id,
        reference_id,
        intent,
        content,
        content_type=None,
        application_id=None,
        application_ref_name=None,
        callback=None,
        partial=None,
        completion_params: ChatCompletionParams = None,
        chat_completion_response: ChatCompletionResponse = None,
        chat_completion_chunk: ChatCompletionChunk = None,
        timing: RequestTimingMetric = None,
        metadata: dict = {},
    ):
        if content_type is None:
            content_type = _get_content_type(content, partial)
        if content_type is None:
            raise Exception("Unable to automatically determine content_type")
        if application_id is None and application_ref_name is None:
            raise Exception("application_id or application_ref_name must be provided")
        eval_request: EvaluateRequest = cls.create_eval_request(
            application_id,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
            partial=partial,
        )
        if completion_params is not None:
            eval_request["chat_completion_request"] = {
                "application_ref_name": application_ref_name,
                "session_id": session_id,
                "reference_id": reference_id,
                "action_type": intent,
                "apply_corrections": False,
                "evaluation_enabled": True,
                "params": completion_params,
                "return_evaluation": True if callback else False,
                "auth_keys": config.auth_keys.model_dump(),
                "metadata": metadata,
            }
            if chat_completion_chunk is not None:
                chat_completion_response = chat_completion_chunk_to_response(
                    chat_completion_chunk, content
                )
            eval_request["chat_completion_response"] = (
                chat_completion_response.model_dump()
            )
        eval_request["timing_metrics"] = timing.model_dump() if timing else None

        cls.run_async(cls.send_evaluation_request_async(eval_request, callback))

    @classmethod
    def stream_correction(
        cls,
        session_id,
        reference_id,
        intent,
        content_type,
        content,
        application_ref_name,
        partial,
        fault_description,
        sentinel_id,
    ):
        eval_request: EvaluateRequest = cls.create_eval_request(
            None,
            application_ref_name,
            session_id,
            reference_id,
            intent,
            content_type,
            content,
            partial=partial,
            fault_description=fault_description,
        )
        eval_request["sentinel_id"] = sentinel_id
        return cls.send_stream_correction_request(eval_request)

    @classmethod
    def create_eval_request(
        cls,
        application_id,
        application_ref_name,
        session_id,
        reference_id,
        intent,
        content_type,
        content,
        partial=None,
        fault_description=None,
        chat_completion_response=None,
    ):
        eval_request = {
            "evaluation_content_type": content_type.value,
            "application_id": application_id,
            "application_ref_name": application_ref_name,
            "session_id": session_id,
            "reference_id": reference_id,
            "action_type": intent,
        }
        if content_type == EvaluationContentType.TEXT:
            if not isinstance(content, str):
                raise Exception("Content must be a string")
            eval_request["text_content"] = content
        elif content_type == EvaluationContentType.MESSAGE:
            eval_request["message_content"] = content
        elif content_type == EvaluationContentType.PARTIAL:
            eval_request["message_content"] = content
            eval_request["text_content"] = partial

        if fault_description:
            eval_request["fault_description"] = fault_description

        return eval_request

    @classmethod
    async def send_evaluation_request_async(
        cls, eval_request: dict, callback: EvaluateCallback = None
    ):
        path = "request" if callback else "submit"
        host = config.maitai_host
        url = f"{host}/evaluation/{path}"

        async def send_request():
            headers = {
                "Content-Type": "application/json",
                "x-api-key": config.api_key,
                "x-client-version": version,
            }
            try:
                async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ssl=False)
                ) as session:
                    async with session.post(
                        url, headers=headers, data=json.dumps(eval_request)
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            cls.log_error(config.api_key, error_text, url)
                            print(
                                f"Failed to send evaluation request. Status code: {response.status}. Error: {error_text}"
                            )
                            return None
                        return await response.read()
            except Exception as e:
                await cls.increment_error(config.api_key, traceback.format_exc(), url)

        result = await send_request()
        if result is not None:
            eval_result = EvaluateResponse.model_validate_json(result)
            if callback is not None:
                try:
                    callback(eval_result)
                except:
                    traceback.print_exc()
            else:
                return eval_result

    @classmethod
    def send_stream_correction_request(
        cls, eval_request: dict
    ) -> Iterable[ChatCompletionChunk]:
        def consume_stream():
            host = config.maitai_host
            url = f"{host}/evaluation/stream_correction"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": config.api_key,
                "x-client-version": version,
            }

            response = requests.post(
                url, headers=headers, data=json.dumps(eval_request), stream=True
            )
            if response.status_code != 200:
                print(
                    f"Failed to send stream correction request. Status code: {response.status_code}. Error: {response.text}"
                )
                cls.log_error(config.api_key, response.text, url)
                return
            try:
                for line in response.iter_lines():
                    if line:
                        yield line
            finally:
                response.close()

        for resp in consume_stream():
            inference_response: ChatCompletionChunk = (
                ChatCompletionChunk.model_validate_json(resp)
            )
            yield inference_response
