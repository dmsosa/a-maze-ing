def centered_positions(
    pattern: tuple[tuple[int, int], ...],
    width: int,
    height: int,
    margin: int = 1,
) -> set[tuple[int, int]]:
    if not pattern:
        return set()

    min_x = min(x for x, _ in pattern)
    max_x = max(x for x, _ in pattern)
    min_y = min(y for _, y in pattern)
    max_y = max(y for _, y in pattern)

    pattern_width = max_x - min_x + 1
    pattern_height = max_y - min_y + 1

    if width < pattern_width + margin * 2:
        return set()

    if height < pattern_height + margin * 2:
        return set()

    center_x = width // 2
    center_y = height // 2

    return {
        (
            center_x + offset_x,
            center_y + offset_y,
        )
        for offset_x, offset_y in pattern
    }
