#!/usr/bin/env python3

import argparse
import logging


def main(args=None) -> None:
    """ """
    while True:
        pass


def parse_args() -> argparse.Namespace:
    """ """
    parser = argparse.ArgumentParser(description="Jetson AI Assistant")
    parser.add_argument(
        "--camera", "-c", type=str, default="/dev/video0", help="Camera sensor"
    )
    # parser.add_argument("--port", type=int, default=5000, help="TCP server port")
    parser.add_argument(
        "--log-level",
        "-ll",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="[%(levelname)s] %(message)s",
    )

    try:
        main(args)
    except KeyboardInterrupt:
        logging.warning("ctrl+c")
        exit(0)
    except Exception as e:
        logging.error(e)
    exit(1)
