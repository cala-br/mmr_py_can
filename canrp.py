import argparse
from genericpath import exists
import json
import logging
from can import Bus

from mmr.can import MmrCan, CanHeader, MessageId
from mmr.can.reverse_proxy import ReverseProxy
from mmr.util import bps


def main():
  args = parse_args()
  if not exists(args.config):
    raise SystemExit('File does not exist')

  with open(args.config) as conf_file:
    config = json.load(conf_file)

  stream = build_stream(config['stream'])
  sink = build_sink(config['sink'])

  proxy = ReverseProxy(stream, sink, {
    0x0: CanHeader(MessageId.ECU.gear),
    0x0: CanHeader(MessageId.ECU.rpm),
    0x0: CanHeader(MessageId.ECU.launch_pit),
    0x0: CanHeader(MessageId.ECU.speed),
    0x0: CanHeader(MessageId.ECU.temp_oil),
    0x0: CanHeader(MessageId.ECU.temp_water),
    0x0: CanHeader(MessageId.ECU.throttle),
    0x0: CanHeader(MessageId.ECU.torque),
  })

  with proxy:
    while True:
      proxy.recv()


def build_stream(config):
  return Bus(
    interface=config['interface'],
    channel=config['channel'],
    bitrate=bps.parse(config['bitrate']),
  )


def build_sink(config):
  return MmrCan(
    interface=config['interface'],
    channel=config['channel'],
    bitrate=config['bitrate'],
  )


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Echoes messages sent from a raw canbus channel to a channel that uses the mmr protocol',
  )

  parser.add_argument('-c', '--config',
    help='Path to the configuration file',
    default='./rp_config.json',
  )

  return parser.parse_args()


if __name__ == '__main__':
  logging.basicConfig(
    level=logging.DEBUG,
  )

  main()