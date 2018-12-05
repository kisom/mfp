def trim(lst, elt=0):
    """Return a list with elt removed off the end."""
    if len(lst) == 0:
        return lst

    i = len(lst) - 1
    while i >= 0:
        if lst[i] != elt:
            break
        i -= 1
    return lst[: i + 1]
