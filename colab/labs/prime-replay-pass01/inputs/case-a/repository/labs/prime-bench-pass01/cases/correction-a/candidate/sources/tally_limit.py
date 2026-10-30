def check_limit(limit: int) -> int:
    """Return the limit or raise Refused (exit 2)."""
    if limit < 0 or limit > 1000:
        raise Refused(f"limit out of range: {limit}")
    return limit
