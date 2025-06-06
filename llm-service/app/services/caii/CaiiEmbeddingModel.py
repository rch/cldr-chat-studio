#
#  CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
#  (C) Cloudera, Inc. 2024
#  All rights reserved.
#
#  Applicable Open Source License: Apache 2.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. ("Cloudera") to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
import json
from typing import Any, List

import httpx
from llama_index.core.base.embeddings.base import BaseEmbedding, Embedding
from pydantic import Field

from .types import Endpoint
from .utils import build_auth_headers


class CaiiEmbeddingModel(BaseEmbedding):
    endpoint: Endpoint = Field(
        Endpoint, description="The endpoint to use for embeddings"
    )
    http_client: httpx.Client = Field(httpx.Client, description="The http client to use for requests")

    def __init__(self, endpoint: Endpoint, http_client: httpx.Client | None = httpx.Client()):
        super().__init__()
        self.endpoint = endpoint
        self.http_client = http_client or httpx.Client()

    def _get_text_embedding(self, text: str) -> Embedding:
        return self._get_embedding(text, "passage")

    async def _aget_query_embedding(self, query: str) -> Embedding:
        raise NotImplementedError("Not implemented")

    def _get_query_embedding(self, query: str) -> Embedding:
        return self._get_embedding(query, "query")

    def _get_embedding(self, query: str, input_type: str) -> Embedding:
        model = self.endpoint.model_name
        body = json.dumps(
            {
                "input": query,
                "input_type": input_type,
                "truncate": "END",
                "model": model,
            }
        )
        structured_response = self.make_embedding_request(body)
        embedding = structured_response["data"][0]["embedding"]
        assert isinstance(embedding, list)
        assert all(isinstance(x, float) for x in embedding)

        return embedding

    def make_embedding_request(self, body: str) -> Any:
        headers = build_auth_headers()
        headers["Content-Type"] = "application/json"
        response = self.http_client.post(url=self.endpoint.url, content=body, headers=headers)
        res = response.content
        json_response = res.decode("utf-8")
        structured_response = json.loads(json_response)
        return structured_response

    def _get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        if len(texts) == 1:
            return [self._get_text_embedding(texts[0])]

        model = self.endpoint.model_name
        body = json.dumps(
            {
                "input": texts,
                "input_type": "passage",
                "truncate": "END",
                "model": model,
            }
        )
        structured_response = self.make_embedding_request(body)

        embeddings = list(
            map(lambda data: data["embedding"], structured_response["data"])
        )
        assert isinstance(embeddings, list)
        assert all(isinstance(x, list) for x in embeddings)
        assert all(all(isinstance(y, float) for y in x) for x in embeddings)

        return embeddings
