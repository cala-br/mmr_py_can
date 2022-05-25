from dataclasses import dataclass

from mmr.can.header import CanHeader


@dataclass
class CanMessage:
  header: CanHeader
  payload: bytes
