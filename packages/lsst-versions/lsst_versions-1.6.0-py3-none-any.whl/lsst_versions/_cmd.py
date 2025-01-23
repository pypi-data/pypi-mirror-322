# This file is part of lsst_versions.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

from __future__ import annotations

import argparse
import logging

from ._versions import _process_version_writing

_LOG = logging.getLogger("lsst_versions")


def build_argparser() -> argparse.ArgumentParser:
    """Construct an argument parser for ``lsst-versions`` command.

    Returns
    -------
    argparser : `argparse.ArgumentParser`
        The argument parser that defines the ``lsst-versions``
        command-line interface.
    """
    parser = argparse.ArgumentParser(description="Determine version information for LSST DM package.")

    parser.add_argument(
        "--log-level",
        default="WARN",
        type=str.upper,
        choices=("WARN", "INFO", "DEBUG"),
        help="Logging level.",
    )

    parser.add_argument(
        "--write-version",
        action="store_true",
        help="Write a version file to the location specified in the pyproject.toml file.",
    )

    parser.add_argument(
        "repo",
        type=str,
        default=".",
        help="Path to package from which to determine the version.",
    )

    return parser


def _run_command(repo: str, write_version: bool) -> str:
    """Run the main command implementation code.

    Parameters
    ----------
    repo : `str`
        Path to a git repository.
    write_version : `bool`
        Whether to write a version file or not.

    Returns
    -------
    version : `str`
        The version string.
    """
    version, written = _process_version_writing(repo, write_version)
    if write_version:
        if written:
            _LOG.info("Written version file to %s", written)
        else:
            _LOG.warning("Unable to write version file.")
    return version


def main() -> None:
    """Run entry point for ``lsst-versions`` command."""
    args = build_argparser().parse_args()

    logging.basicConfig(level=args.log_level)

    version = _run_command(args.repo, args.write_version)
    print(version)
