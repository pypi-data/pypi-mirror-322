from typing import Any, Union, Optional

from pytoniq_core import Address, Cell, StateInit, begin_cell

from ..models import Message
from ...utils import boc_to_base64_string, to_nano


def create_transfer_message(
        destination: Union[Address, str],
        amount: Union[float, int],
        body: Optional[Union[Cell, str]] = None,
        state_init: Optional[StateInit] = None,
        **_: Any,
) -> Message:
    """
    Creates a basic transfer message compatible with the SendTransactionRequest.

    :param destination: The Address object or string representing the recipient.
    :param amount: The amount in TONs to be transferred.
    :param body: Optional message payload (Cell or string).
    :param state_init: Optional StateInit for deploying contracts.
    :param _: Any additional keyword arguments are ignored.
    :return: A Message object ready to be sent.
    """
    destination_str = destination.to_str() if isinstance(destination, Address) else destination
    state_init_b64 = boc_to_base64_string(state_init.serialize().to_boc()) if state_init else None

    if body is not None:
        if isinstance(body, str):
            # Convert string payload to a Cell.
            body_cell = (
                begin_cell()
                .store_uint(0, 32)
                .store_snake_string(body)
                .end_cell()
            )
            body = boc_to_base64_string(body_cell.to_boc())
        else:
            # Body is already a Cell; convert to base64.
            body = boc_to_base64_string(body.to_boc())

    message = Message(
        address=destination_str,
        amount=str(to_nano(amount)),
        payload=body,
        state_init=state_init_b64,
    )
    return message
