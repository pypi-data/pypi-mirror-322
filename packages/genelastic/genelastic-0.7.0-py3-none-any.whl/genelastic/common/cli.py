"""Utility functions for CLI scripts."""

import argparse


def add_verbose_control_args(parser: argparse.ArgumentParser) -> None:
    """Add verbose control arguments to the parser.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_const",
        const=0,
        default=1,
        help="Set verbosity to 0 (quiet mode).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="count",
        default=1,
        help=(
            "Verbose level. -v for information, -vv for debug, -vvv for trace."
        ),
    )


def add_es_connection_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to the parser needed to gather ElasticSearch server connection parameters.
    Arguments are added to the parser by using its reference.
    """
    parser.add_argument(
        "--es-host",
        dest="es_host",
        default="localhost",
        help="Address of Elasticsearch host.",
    )
    parser.add_argument(
        "--es-port",
        type=int,
        default=9200,
        dest="es_port",
        help="Elasticsearch port.",
    )
    parser.add_argument(
        "--es-usr", dest="es_usr", default="elastic", help="Elasticsearch user."
    )
    parser.add_argument(
        "--es-pwd", dest="es_pwd", required=True, help="Elasticsearch password."
    )
    parser.add_argument(
        "--es-cert-fp",
        dest="es_cert_fp",
        help="Elasticsearch sha256 certificate fingerprint.",
    )
    parser.add_argument(
        "--es-index-prefix",
        dest="es_index_prefix",
        help="Add the given prefix to each index created during import.",
    )
