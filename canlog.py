#!/usr/bin/python3
import argparse
import logging
import struct
from typing import Optional

from mmr.can import MmrCan, Channel, Interface
from mmr.can.header import CanHeader
from mmr.util.enums import desc_enum


def main():
  args = parse_args()
  can = MmrCan(args.interface, args.channel, args.bitrate)
  with can:
    while True:
      receive_one(can, args.format)


def receive_one(can: MmrCan, format: Optional[str]):
  msg = can.recv()
  if not msg:
    return

  header = msg.header
  payload =\
    msg.payload.hex(' ') if format is None else struct.unpack(format, msg.payload)

  log_message(header, payload)


def log_message(header: CanHeader, payload: str):
  logging.info(f'{header=} | {payload}')


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Logs can messages sent with mmr\'s custom protocol',
  )

  parser.add_argument('--interface',
    help=f'The can interface. Possible values: {desc_enum(Interface)}',
    default=Interface.socketcan.value,
  )

  parser.add_argument('--channel',
    help=f'The channel',
    default=Channel.can0.value,
  )

  parser.add_argument('--bitrate',
    help='The bitrate, in bits per second',
    default='1mbps',
  )

  parser.add_argument('--format',
    help='The format to pass to struct.unpack',
    default=None,
  )

  return parser.parse_args()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
  )

  main()