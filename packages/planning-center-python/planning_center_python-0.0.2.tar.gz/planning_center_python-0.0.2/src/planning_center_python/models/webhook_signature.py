from collections.abc import Mapping
from hashlib import sha256
import hmac
from typing import Any, Union

from planning_center_python.errors import SignatureVerificationError

SIGNATURE_HEADER = "X-PCO-Webhooks-Authenticity"


class WebhookSignature(object):
    """Represents the signature of a webhook from PCO. Can validate that the webhook is
    valid and signed correctly.
    """

    @staticmethod
    def _compute_signature(payload: str, secret: str) -> str:
        mac = hmac.new(
            secret.encode("utf-8"),
            msg=payload.encode("utf-8"),
            digestmod=sha256,
        )
        return mac.hexdigest()

    @staticmethod
    def _get_header_signature(header: Mapping[str, Any]) -> Union[Any, None]:
        return header.get(SIGNATURE_HEADER)

    @classmethod
    def verify(cls, payload: str, headers: Mapping[str, Any], secret: str) -> bool:
        """Verifies the authenticity of a PCO generated webhook. Based on the webhook
        signing documented here https://developer.planning.center/docs/#/overview/webhooks.

        Args:
            payload (str): A json representation of the payload (body) included in the request
            headers (Mapping[str, Any]): A dictionary of the headers included in the request.
            secret (str): The secret provided by PCO for signing webhooks for those events.

        Raises:
            SignatureVerificationError: The message of the exception will include the a description
                of the error. Also the header signature (if available) and the body will be included.

        Returns:
            bool: A boolean indicating if the webhook is valid (True) or invalid (False)
        """
        try:
            signature = cls._get_header_signature(headers)
        except Exception:
            raise SignatureVerificationError(
                "Error parsing signature from header", "", payload
            )

        if not signature:
            raise SignatureVerificationError(
                "Could not find signature header", "", payload
            )

        if not isinstance(signature, str):
            raise SignatureVerificationError(
                "Invalid signature included in the headers", signature, payload
            )

        try:
            computed_signature = cls._compute_signature(payload, secret)
        except Exception:
            raise SignatureVerificationError(
                "Error computing signature", signature, payload
            )

        return hmac.compare_digest(signature, computed_signature)
