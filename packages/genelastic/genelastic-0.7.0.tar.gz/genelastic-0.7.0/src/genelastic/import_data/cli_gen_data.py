import argparse
import logging
from pathlib import Path

from genelastic.common import add_verbose_control_args

from .logger import configure_logging
from .random_bundle import (
    RandomBundle,
)

logger = logging.getLogger("genelastic")


def read_args() -> argparse.Namespace:
    """Read arguments from command line."""
    parser = argparse.ArgumentParser(
        description="Genetics data random generator.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    add_verbose_control_args(parser)
    parser.add_argument(
        "-d",
        "--data-folder",
        dest="data_folder",
        required=True,
        help="Data destination folder.",
        type=Path,
    )
    parser.add_argument(
        "--log-file", dest="log_file", help="Path to a log file."
    )
    parser.add_argument(
        "-n",
        "--chrom-nb",
        dest="chrom_nb",
        type=int,
        default=5,
        help="Number of chromosomes to include in the generated VCF file.",
    )
    parser.add_argument(
        "-o",
        "--output-yaml-file",
        dest="output_file",
        default=None,
        help="Output YAML file.",
        type=Path,
    )
    parser.add_argument(
        "-s",
        "--sequence-size",
        type=int,
        default=2000,
        help="Sequence size (number of nucleotides) generated for each chromosome.",
    )
    parser.add_argument(
        "-c",
        "--coverage",
        action="store_true",
        help="Generate a coverage file for each analysis.",
    )
    parser.add_argument(
        "-a",
        "--analyses",
        help="Number of analyses to generate. "
        "Each analysis is composed of a YAML bundle file declaring its wet lab and bioinformatics processes, "
        "a VCF file and optionally a coverage file.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--processes",
        help="Number of Wet Lab and Bioinformatics processes to generate.",
        default=1,
        type=int,
    )
    return parser.parse_args()


def main() -> None:
    """Entry point of the gen-data script."""
    # Read command line arguments
    args = read_args()
    folder = args.data_folder.resolve()

    if not folder.is_dir():
        msg = f"ERROR: '{folder}' does not exist or is not a directory."
        raise SystemExit(msg)

    if args.analyses < 1:
        msg = "Analyses count must be at least 1."
        raise SystemExit(msg)

    if args.processes < 1:
        msg = "Processes count must be at least 1."
        raise SystemExit(msg)

    # Configure logging
    configure_logging(args.verbose, log_file=args.log_file)
    logger.debug("Arguments: %s", args)

    # Write to stdout or file
    RandomBundle(
        folder,
        args.analyses,
        args.processes,
        args.chrom_nb,
        args.sequence_size,
        do_gen_coverage=args.coverage,
    ).to_yaml(args.output_file)


if __name__ == "__main__":
    main()
