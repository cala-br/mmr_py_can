from typing import List, Type


def list_enum(enum: Type) -> List[str]:
  return [e.value for e in enum]


def desc_enum(enum: Type) -> str:
  return ', '.join(list_enum(enum))