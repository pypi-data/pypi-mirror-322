import traceback
from typing import Any, Callable, Awaitable

import grpc  # type: ignore
from google.protobuf.json_format import MessageToDict

from ...._utils.logs import logger
from ...._protos.remote_layer.remote_layer_pb2 import (
    CallRequest,
    InitRequest,
    CallResponse,
    InitResponse,
)
from ...._protos.remote_layer.remote_layer_pb2_grpc import RemoteLayerServicer as _RemoteLayerServicer  # type: ignore


class RemoteLayerServicer(_RemoteLayerServicer):
    """
    gRPC servicer for remote callable layer operations.

    Parameters
    ----------
    on_call : Callable[..., Awaitable[Any]]
        The lambda layer to be used for the remote callable layer.
    on_init : Callable[..., Awaitable[Any]] | None, optional
        The lambda layer to be used for the remote callable layer.
    """

    def __init__(self, on_call: Callable[..., Awaitable[Any]], on_init: Callable[..., Awaitable[Any]] | None = None):
        self._on_call = on_call
        self._on_init = on_init
        self._initialized = False if on_init else True

    async def Init(
        self, request: InitRequest, context: grpc.aio.ServicerContext[Any, Any]  # noqa: ARG002
    ) -> InitResponse:
        """
        Initialize the server with settings.

        Parameters
        ----------
        request : remote_layer_pb2.InitRequest
            Configuration request containing node settings.
        context : grpc.aio.ServicerContext
            gRPC service context.

        Returns
        -------
        remote_node_pb2.ConfigureResponse
            Response indicating success or failure of configuration.
        """
        try:
            logger.info("Initializing layer...")
            settings = MessageToDict(request.settings)

            if self._on_init:
                await self._on_init(self, **settings)
            self._initialized = True

            logger.debug(f"Initialized successfully with settings: {settings}")
            return InitResponse(success=True)

        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            logger.error(traceback.format_exc())
            return InitResponse(success=False, error_message=str(e))

    async def Call(
        self, request: CallRequest, context: grpc.aio.ServicerContext[Any, Any]  # noqa: ARG002
    ) -> CallResponse:
        """
        Process a single step with the configured node.

        Parameters
        ----------
        request : remote_node_pb2.StepRequest
            Request containing the target frame to process.
        context : grpc.aio.ServicerContext
            gRPC service context.

        Returns
        -------
        remote_node_pb2.StepResponse
            Response containing the processed frame or error message.
        """
        if not self._initialized:
            logger.error("Layer not initialized. Call Init first.")
            return CallResponse(success=False, error_message="Layer not initialized. Call Init first.")

        try:
            y: Any | None = await self._on_call(self, request.x)
            return CallResponse(success=True, y=bytes(y) if y else None)
        except Exception as e:
            logger.error(f"Error during Call: {e}")
            logger.error(traceback.format_exc())
            return CallResponse(success=False, error_message=str(e))

    @property
    def initialized(self) -> bool:
        return self._initialized
