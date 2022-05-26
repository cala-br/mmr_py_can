import logging
from typing import Dict, Optional
from can import Bus

from mmr.can.can import MmrCan
from mmr.can.header import CanHeader


class ReverseProxy:
  def __init__(self, stream: Bus, sink: MmrCan, id_map: Dict[int, CanHeader]):
    self._stream = stream
    self._sink = sink
    self._id_map = id_map

  
  def recv(self, timeout: Optional[float] = None) -> None:
    msg = self._stream.recv(timeout)
    if msg is None:
      logging.debug('Timed out')
      return

    canId = msg.arbitration_id
    payload = msg.data
    logging.debug(f'Received {canId=} | {payload}')
    if canId not in self._id_map:
      logging.debug(f'Dropped {canId=}')
      return

    header = self._id_map[canId]
    self._sink.send(header, payload)
    logging.debug(f'Redirected {canId=} as {header=}')


  def __enter__(self) -> 'ReverseProxy':
    self._stream.__enter__()
    self._sink.__enter__()
    return self


  def __exit__(self) -> None:
    self._sink.__exit__()
    self._stream.__exit__()
