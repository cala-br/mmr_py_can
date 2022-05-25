from dataclasses import dataclass
from enum import IntEnum
from colorama import Fore

from mmr.can.message_id import MessageId


class Priority(IntEnum):
  low = 0b010
  normal = 0b001
  high = 0b000


class MessageType(IntEnum):
  scs = 0b000
  ack = 0b001
  multi_frame = 0b010
  multi_frame_end = 0b011
  normal = 0b100


@dataclass
class CanHeader:
  message_id: MessageId
  sender_id: int = 0
  seq_number: int = 0
  message_type: MessageType = MessageType.normal
  priority: Priority = Priority.normal


  def to_bits(self) -> int:
    return (0
      | self.priority << 26
      | self.message_id << 16
      | self.sender_id << 6
      | self.seq_number << 3
      | self.message_type
    )

  
  @staticmethod
  def from_bits(bits: int) -> 'CanHeader':
    return CanHeader(
      priority = bits >> 26,
      message_id = bits >> 16,
      sender_id = bits >> 6,
      seq_number = bits >> 3,
      message_type = bits,
    )


  def __repr__(self) -> str:
    return (f'''(
        {Fore.GREEN}{repr(self.priority)}{Fore.RESET}, \
        {Fore.BLUE}message_id={self.message_id}{Fore.RESET}, \
        {Fore.RED}sender_id={self.sender_id}{Fore.RESET}, \
        {Fore.CYAN}seq_number={self.seq_number}{Fore.RESET}, \
        {Fore.MAGENTA}{repr(self.message_type)}{Fore.RESET}
      )'''
      .replace('\n', '')
      .replace('  ', '')
      .replace('\t', '')
    )