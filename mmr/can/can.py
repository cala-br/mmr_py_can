from enum import Enum
from typing import Optional
from can import Bus, Message

from mmr.can.header import CanHeader
from mmr.can.message import CanMessage
from mmr.util import bps


class Interface(str, Enum):
  socketcan = 'socketcan'
  pcan = 'pcan'
  ixxat = 'ixxat'
  vector = 'vector'


class Channel(str, Enum):
  can0 = 'can0'
  can1 = 'can1'


class MmrCan:
  def __init__(self,
    interface: Interface,
    channel: Channel,
    bitrate: int | str,
    **kwargs
  ):
    self._bus = Bus(
      interface=interface,
      channel=channel,
      bitrate=bps.parse(bitrate),
      **kwargs
    )


  def send(self, header: CanHeader, payload: bytes) -> None:
    self._bus.send(Message(
      arbitration_id=header.to_bits(),
      is_extended_id=True,
      dlc=len(payload),
      data=payload,
    ))


  def recv(self, timeout: Optional[float] = None) -> Optional[CanMessage]:
    msg = self._bus.recv(timeout)
    if msg is None:
      return None

    return CanMessage(
      header=CanHeader.from_bits(msg.arbitration_id),
      payload=msg.data,
    )


  def __enter__(self) -> 'MmrCan':
    self._bus.__enter__()
    return self

  
  def __exit__(self) -> None:
    self._bus.__exit__()