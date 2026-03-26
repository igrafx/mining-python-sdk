# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import pytest
from unittest.mock import patch, MagicMock
import requests as req
from igrafx_mining_sdk.api_connector import APIConnector, InvalidRouteError


def _make_connector():
    """Create an APIConnector instance without calling __init__ (which would try to authenticate)."""
    conn = APIConnector.__new__(APIConnector)
    conn.apiurl = "https://example.com/pub"
    conn.ssl_verify = True
    conn.token_header = {"Authorization": "Bearer fake"}
    conn.wg_id = "test_wg"
    conn.wg_key = "test_key"
    conn._authurl = "https://auth.example.com"
    return conn


class TestAPIConnector:
    """Tests for APIConnector class — offline, no server dependency."""

    # --- InvalidRouteError ---

    def test_invalid_route_error_default(self):
        """Test InvalidRouteError with default message"""
        err = InvalidRouteError()
        assert err.message == "Unauthorized to use this route"

    def test_invalid_route_error_custom(self):
        """Test InvalidRouteError with custom message"""
        err = InvalidRouteError("custom error")
        assert err.message == "custom error"

    # --- __login error handling ---

    # Replaces the req module (which is import requests as req)
    # inside api_connector.py with a MagicMock for the duration of the test.
    @patch('igrafx_mining_sdk.api_connector.req')
    def test_login_http_error_bad_request(self, mock_req):
        """Test that __login raises Exception on Bad Request"""
        mock_response = MagicMock()
        mock_response.reason = "Bad Request"
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError(response=mock_response)
        mock_req.post.return_value = mock_response
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        with pytest.raises(Exception, match="Invalid login credentials"):
            conn._APIConnector__login()

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_login_http_error_non_bad_request(self, mock_req):
        """Test that __login returns None on non-Bad Request HTTPError"""
        mock_response = MagicMock()
        mock_response.reason = "Forbidden"
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError(response=mock_response)
        mock_req.post.return_value = mock_response
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        result = conn._APIConnector__login()
        assert result is None

    # --- get_request 401 retry ---

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_get_request_401_retry(self, mock_req):
        """Test that get_request retries with new token on 401"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.raise_for_status = MagicMock()

        mock_req.get.side_effect = [mock_401, mock_200]
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        conn._APIConnector__login = MagicMock(return_value={"Authorization": "Bearer new"})

        conn.get_request("/test")
        conn._APIConnector__login.assert_called_once()

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_get_request_401_max_retries(self, mock_req):
        """Test that get_request raises InvalidRouteError after max retries (caught internally)"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_401.text = "Unauthorized"
        mock_401.raise_for_status = MagicMock()

        mock_req.get.return_value = mock_401
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        result = conn.get_request("/test", nblasttries=3, maxtries=3)
        assert result is not None

    # --- post_request 401 retry ---

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_post_request_401_retry(self, mock_req):
        """Test that post_request retries with new token on 401"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.raise_for_status = MagicMock()

        mock_req.post.side_effect = [mock_401, mock_200]
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        conn._APIConnector__login = MagicMock(return_value={"Authorization": "Bearer new"})

        conn.post_request("/test")
        conn._APIConnector__login.assert_called_once()

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_post_request_401_max_retries(self, mock_req):
        """Test that post_request raises InvalidRouteError after max retries (caught internally)"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_401.text = "Unauthorized"
        mock_401.raise_for_status = MagicMock()

        mock_req.post.return_value = mock_401
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        result = conn.post_request("/test", nblasttries=3, maxtries=3)
        assert result is not None

    # --- delete_request 401 retry ---

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_delete_request_401_retry(self, mock_req):
        """Test that delete_request retries with new token on 401"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.raise_for_status = MagicMock()

        mock_req.delete.side_effect = [mock_401, mock_200]
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        conn._APIConnector__login = MagicMock(return_value={"Authorization": "Bearer new"})

        conn.delete_request("/test")
        conn._APIConnector__login.assert_called_once()

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_delete_request_401_max_retries(self, mock_req):
        """Test that delete_request raises InvalidRouteError after max retries (caught internally)"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_401.text = "Unauthorized"
        mock_401.raise_for_status = MagicMock()

        mock_req.delete.return_value = mock_401
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        result = conn.delete_request("/test", nblasttries=3, maxtries=3)
        assert result is not None

    # --- put_request 401 retry ---

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_put_request_401_retry(self, mock_req):
        """Test that put_request retries with new token on 401"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.raise_for_status = MagicMock()

        mock_req.put.side_effect = [mock_401, mock_200]
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        conn._APIConnector__login = MagicMock(return_value={"Authorization": "Bearer new"})

        conn.put_request("/test")
        conn._APIConnector__login.assert_called_once()

    @patch('igrafx_mining_sdk.api_connector.req')
    def test_put_request_401_max_retries(self, mock_req):
        """Test that put_request raises InvalidRouteError after max retries (caught internally)"""
        mock_401 = MagicMock()
        mock_401.status_code = 401
        mock_401.text = "Unauthorized"
        mock_401.raise_for_status = MagicMock()

        mock_req.put.return_value = mock_401
        mock_req.HTTPError = req.HTTPError
        mock_req.exceptions = req.exceptions

        conn = _make_connector()
        result = conn.put_request("/test", nblasttries=3, maxtries=3)
        assert result is not None
