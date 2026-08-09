from requests import Response, Session
from requests.exceptions import RequestException

from ..config import settings
from ..utils import get_logger


logger = get_logger(__name__)


class APIClient:
    """
    HTTP client for communicating with external APIs.
    """

    def __init__(self) -> None:
        self.base_url = settings.API_BASE_URL.rstrip("/")
        self.timeout = settings.API_TIMEOUT

        self.session = Session()

    def get(self, endpoint: str) -> Response:
        """
        Send a GET request to the specified API endpoint.

        Args:
            endpoint: API endpoint path, e.g. "/products".

        Returns:
            The HTTP response.

        Raises:
            RequestException: If the request fails or returns
                an unsuccessful HTTP status code.
        """
        url = f"{self.base_url}{endpoint}"

        logger.info(
            "Making GET request to %s (timeout=%ss)",
            url,
            self.timeout,
        )

        try:
            response = self.session.get(
                url=url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            logger.info(
                "Received response with status code %s",
                response.status_code,
            )

            return response

        except RequestException:
            logger.exception("Request to %s failed", url)
            raise

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
        logger.info("API client session closed.")