from __future__ import annotations

import logging
from collections.abc import Collection, Sequence
from copy import copy
from types import TracebackType
from typing import Optional, Self, Type

from .exception import DiagnosticException, T
from .models import DiagnosticError, Loc


class DiagnosticCollector:
    """
    Diagnostic collector, that catches errors. Can be used as context manager, then it raises automatically
    at the __exit__ of the with block. Or can be used manually without context manager, then just call
    self.raise_if_errors().

    Example:

    >>> with DiagnosticCollector() as diag:
    >>>     diag.append(DiagnosticError(loc=["somewhere"], msg="There was an error.", type="error"))
    >>> # Here, DiagnosticException is raised.

    Or:

    >>> diag = DiagnosticCollector()
    >>> diag.append(DiagnosticError(loc=["somewhere"], msg="There was an error.", type="error"))
    >>> diag.raise_if_errors()  # Here, DiagnosticException is raised.

    Diagnostic collectors can be nested, and errors from inner collectors are included in outer collector.
    """

    def __init__(
        self,
        *,
        prefix: Optional[Loc] = None,
        strip_prefix: Optional[Loc] = None,
        strip_prefixes: Optional[Collection[Loc]] = None,
        suffix: Optional[Loc] = None,
        strip_suffix: Optional[Loc] = None,
        strip_suffixes: Optional[Collection[Loc]] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        :param prefix: Add specified prefix to all errors in this collector.
        :param strip_prefix: Strip specified prefix from all errors in this collector, including errors from inner collectors.
        :param strip_prefixes: Strip specified prefixes from all errors in this collector, including errors from inner collectors
            (using this argument, you can specify multiple different prefixes to be stripped).
        :param suffix: Add specified suffix to all errors in this collector.
        :param strip_suffix: Strip specified suffix from all errors in this collector, including errors from inner collectors.
        :param strip_suffixes: Strip specified suffixes from all errors in this collector, including errors from inner collectors
            (using this argument, you can specify multiple different suffixes to be stripped).
        """

        if not isinstance(prefix, list) and prefix is not None:  # type: ignore[unreachable]  # mypy does not ensure runtime check
            raise AttributeError("Prefix must be a list of locations.")

        self.prefix: Optional[Loc] = prefix
        self.strip_prefixes: list[Loc] = ([strip_prefix] if strip_prefix else []) + list(strip_prefixes or [])
        self.suffix: Optional[Loc] = suffix
        self.strip_suffixes: list[Loc] = ([strip_suffix] if strip_suffix else []) + list(strip_suffixes or [])

        self.errors: list[DiagnosticError] = []

        # Set to true in raise_if_errors, to prevent doubling of errors when context manager catches own exception.
        self._raised_from_self = False

        self.logger = logger or logging.root

    def _resolve_prefix_and_suffix(
        self, prefix: Optional[Loc] = None, suffix: Optional[Loc] = None
    ) -> tuple[Optional[Loc], Optional[Loc]]:
        return prefix or self.prefix, suffix or self.suffix

    def _append(self, error: DiagnosticError, prefix: Optional[Loc] = None, suffix: Optional[Loc] = None) -> None:
        """
        Append error to diagnostics.
        :param error: Error to be appended.
        :param prefix: Prefix to prepend to error location.
        :param suffix: Suffix to append to error location.
        """
        if not isinstance(error, DiagnosticError):
            raise AttributeError("DiagnosticCollector can accept only DiagnosticErrors.")

        if self.strip_prefixes:
            for strip_prefix in self.strip_prefixes:
                if error.loc[0 : len(strip_prefix)] == strip_prefix:
                    error = error.model_copy(update={"loc": error.loc[len(strip_prefix) :]})
                    break

        if self.strip_suffixes:
            for strip_suffix in self.strip_suffixes:
                if error.loc[-len(strip_suffix) :] == strip_suffix:
                    error = error.model_copy(update={"loc": error.loc[: -len(strip_suffix)]})

        prefix, suffix = self._resolve_prefix_and_suffix(prefix, suffix)

        if prefix:
            error = error.model_copy(update={"loc": prefix + error.loc})

        if suffix:
            error = error.model_copy(update={"loc": error.loc + suffix})

        self.errors.append(error)

    def append(
        self, error: DiagnosticError, prefix: Optional[Loc] = None, suffix: Optional[Loc] = None, stacklevel: int = 0
    ) -> Self:
        """
        Append new error to the collector, optionally prefixing it with specified prefix or suffixing it with specified suffix.
        :param error: Error to be added.
        :param prefix: Prefix to be prepended before error's loc. If specified, overwrites class-level prefix.
        :param suffix: Suffix to be appended to error's loc. If specified, overwrites class-level suffix.
        :param stacklevel: Optional stacklevel for logging (default 0).
        :return: Self for chaining
        """
        prefix, suffix = self._resolve_prefix_and_suffix(prefix, suffix)

        if prefix and suffix:
            self.logger.debug(
                "Appending error with prefix %s and suffix %s: %s", prefix, suffix, error, stacklevel=stacklevel + 2
            )
        elif prefix:
            self.logger.debug("Appending error with prefix %s: %s", prefix, suffix, stacklevel=stacklevel + 2)
        elif suffix:
            self.logger.debug("Appending error with suffix %s: %s", suffix, error, stacklevel=stacklevel + 2)
        else:
            self.logger.debug("Appending error: %s", error, stacklevel=stacklevel + 2)

        self._append(error, prefix, suffix)

        return self

    def add(
        self, error: DiagnosticError, prefix: Optional[Loc] = None, suffix: Optional[Loc] = None, stacklevel: int = 0
    ) -> Self:
        """Alias for append()"""
        return self.append(error, prefix, suffix, stacklevel + 1)

    def include(
        self,
        other: DiagnosticCollector | DiagnosticException[T] | Sequence[DiagnosticError],
        prefix: Optional[Loc] = None,
        suffix: Optional[Loc] = None,
    ) -> Self:
        """
        Include errors from other diagnostic response, optionally prefixing errors with location.
        :param other: Other diagnostic to include.
        :param prefix: Error prefix. Overrides class-level prefix.
        :param suffix: Error suffix. Overrides class-level suffix.
        :return: Self for chaining
        """
        errors: list[DiagnosticError] = []

        if isinstance(other, DiagnosticCollector):
            if other == self:
                return self

            errors.extend(other.errors)

            # As errors are processed by including in this collector, clear errors from other, to avoid raising exception.
            other.errors = []
        elif isinstance(other, DiagnosticException):
            errors.extend(other.errors())
        elif not isinstance(other, Sequence):
            raise AttributeError(
                "DiagnosticCollector can accept only other DiagnosticCollectior, DiagnosticException or sequence of "
                "DiagnosticErrors."
            )
        else:
            errors.extend(other)

        prefix, suffix = self._resolve_prefix_and_suffix(prefix, suffix)

        for error in errors:
            self._append(error, prefix, suffix)

            if prefix and suffix:
                self.logger.debug(
                    "Including error from nested diagnostics with prefix %s and suffix %s: %s", prefix, suffix, error
                )
            elif prefix:
                self.logger.debug("Including error from nested diagnostics with prefix %s: %s", prefix, error)
            elif suffix:
                self.logger.debug("Including error from nested diagnostics with suffix %s: %s", suffix, error)
            else:
                self.logger.debug("Including error from nested diagnostics: %s", error)

        return self

    def raise_if_errors(self) -> None:
        """
        Raises DiagnosticException if there are any collected errors. Otherwise, does nothing.
        """
        if bool(self):
            self._raised_from_self = True
            raise DiagnosticException(detail=copy(self.errors))

    def __bool__(self) -> bool:
        """
        Whether the exception contains any error, therefore should be raised.
        """
        return bool(self.errors)

    def __enter__(self) -> DiagnosticCollector:
        """
        Start context manager. At end of context, DiagnosticException is automatically raised when there are any errors.
        """
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """
        Automatically raises DiagnosticException if there is any diagnostic to be presented.

        If __exit__ occured because of another DiagnosticException, append errors from it to this diagnostic
        (with optionally specified prefix) and re-raise new DiagnosticException with all collected errors.
        """
        # Include errors from inner exception.
        if isinstance(exc_val, DiagnosticException):
            if not self._raised_from_self:
                self.include(exc_val.errors())

        # Do not raise DiagnosticException if other exception (other than DiagnosticException) was raised,
        # as we don't want to shadow internal exceptions from user even if there are some diagnostics.
        if exc_val is None or isinstance(exc_val, DiagnosticException):
            self.raise_if_errors()

    async def __aenter__(self) -> DiagnosticCollector:
        """
        Async version of context manager. See __enter__().
        """
        return self.__enter__()

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """
        Async version of context manager. See __exit__().
        """
        self.__exit__(exc_type, exc_val, exc_tb)
