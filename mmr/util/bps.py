__multipliers = {
  'mbps': 1_000_000,
  'kbps': 1_000,
}


def parse(bitrate: int | str) -> int:
  if isinstance(bitrate, int):
    return bitrate

  if isinstance(bitrate, str):
    return _parse_str(bitrate)

  raise TypeError()


def _parse_str(bitrate: str) -> int:
  mult = _get_multiplier(bitrate)
  base = _get_base(bitrate, mult)

  return base * __multipliers[mult]


def _get_multiplier(bitrate: str) -> str:
  return next(r
    for r in __multipliers.keys()
    if bitrate.endswith(r)
  )


def _get_base(bitrate: str, suffix: str) -> int:
  return int(bitrate.replace(suffix, ''))