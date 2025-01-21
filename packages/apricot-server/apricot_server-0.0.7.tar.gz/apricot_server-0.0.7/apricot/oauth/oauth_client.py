from __future__ import annotations

import os
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Self

import requests
from oauthlib.oauth2 import (
    BackendApplicationClient,
    InvalidGrantError,
    LegacyApplicationClient,
    TokenExpiredError,
)
from requests_oauthlib import OAuth2Session
from twisted.python import log

if TYPE_CHECKING:
    from apricot.cache import UidCache
    from apricot.types import JSONDict


class OAuthClient(ABC):
    """Base class for OAuth client talking to a generic backend."""

    def __init__(
        self: Self,
        client_id: str,
        client_secret: str,
        debug: bool,  # noqa: FBT001
        redirect_uri: str,
        scopes_application: list[str],
        scopes_delegated: list[str],
        token_url: str,
        uid_cache: UidCache,
    ) -> None:
        """Initialise an OAuthClient.

        @param client_id: OAuth client ID
        @param client_secret: OAuth client secret
        @param debug: Enable debug output
        @param redirect_uri: OAuth redirect URI
        @param scopes: OAuth scopes
        @param token_url: OAuth token URL
        @param uid_cache: Cache for UIDs
        """
        # Set attributes
        self.bearer_token_: str | None = None
        self.client_secret = client_secret
        self.debug = debug
        self.token_url = token_url
        self.uid_cache = uid_cache
        # Allow token scope to not match requested scope. (Other auth libraries allow
        # this, but Requests-OAuthlib raises exception on scope mismatch by default.)
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"  # noqa: S105
        os.environ["OAUTHLIB_IGNORE_SCOPE_CHANGE"] = "1"

        try:
            # OAuth client that uses application credentials
            if self.debug:
                log.msg("Initialising application credential client.")
            self.session_application = OAuth2Session(
                client=BackendApplicationClient(
                    client_id=client_id,
                    scope=scopes_application,
                    redirect_uri=redirect_uri,
                ),
            )
        except Exception as exc:
            msg = f"Failed to initialise application credential client.\n{exc!s}"
            raise RuntimeError(msg) from exc

        try:
            # OAuth client that uses delegated credentials
            if self.debug:
                log.msg("Initialising delegated credential client.")
            self.session_interactive = OAuth2Session(
                client=LegacyApplicationClient(
                    client_id=client_id,
                    scope=scopes_delegated,
                    redirect_uri=redirect_uri,
                ),
            )
        except Exception as exc:
            msg = f"Failed to initialise delegated credential client.\n{exc!s}"
            raise RuntimeError(msg) from exc

    @property
    def bearer_token(self: Self) -> str:
        """Return a bearer token, requesting a new one if necessary."""
        try:
            if not self.bearer_token_:
                log.msg("Requesting a new authentication token from the OAuth backend.")
                json_response = self.session_application.fetch_token(
                    token_url=self.token_url,
                    client_id=self.session_application._client.client_id,
                    client_secret=self.client_secret,
                )
                self.bearer_token_ = self.extract_token(json_response)
        except Exception as exc:
            msg = f"Failed to fetch bearer token from OAuth endpoint.\n{exc!s}"
            raise RuntimeError(msg) from exc
        else:
            return self.bearer_token_

    @staticmethod
    @abstractmethod
    def extract_token(json_response: JSONDict) -> str:
        """Extract the bearer token from an OAuth2Session JSON response."""

    @abstractmethod
    def groups(self: Self) -> list[JSONDict]:
        """Return JSON data about groups from the OAuth backend.

        This should be a list of JSON dictionaries where 'None' is used to signify missing values.
        """

    @abstractmethod
    def users(self: Self) -> list[JSONDict]:
        """Return JSON data about users from the OAuth backend.

        This should be a list of JSON dictionaries where 'None' is used to signify missing values.
        """

    def query(
        self: Self,
        url: str,
        *,
        use_client_secret: bool = True,
    ) -> dict[str, Any]:
        """Make a query against the OAuth backend."""
        kwargs = (
            {
                "client_id": self.session_application._client.client_id,
                "client_secret": self.client_secret,
            }
            if use_client_secret
            else {}
        )
        return self.request(
            url=url,
            method="GET",
            **kwargs,
        )

    def request(
        self: Self,
        *args: Any,
        method: str = "GET",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make a request to the OAuth backend."""

        def query_(*args: Any, **kwargs: Any) -> requests.Response:
            return self.session_application.request(  # type: ignore[no-any-return]
                method,
                *args,
                **kwargs,
                headers={"Authorization": f"Bearer {self.bearer_token}"},
            )

        try:
            result = query_(*args, **kwargs)
            result.raise_for_status()
        except (TokenExpiredError, requests.exceptions.HTTPError):
            log.msg("Authentication token has expired.")
            self.bearer_token_ = None
            result = query_(*args, **kwargs)
        if result.status_code == HTTPStatus.NO_CONTENT:
            return {}
        return result.json()  # type: ignore[no-any-return]

    def verify(self: Self, username: str, password: str) -> bool:
        """Verify username and password by attempting to authenticate against the OAuth backend."""
        try:
            self.session_interactive.fetch_token(
                token_url=self.token_url,
                username=username,
                password=password,
                client_id=self.session_interactive._client.client_id,
                client_secret=self.client_secret,
            )
        except InvalidGrantError as exc:
            log.msg(f"Authentication failed for user '{username}'.\n{exc}")
            return False
        else:
            return True
