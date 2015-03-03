KB = 1024

def format_memory(val):
    """Pretty formatting of memory."""
    val = float(val)
    if val < KB:
        label = "B"
    elif KB < val < KB ** 2:
        label = "KB"
        val /= KB
    elif KB ** 2 < val < KB ** 3:
        label = "MB"
        val /= KB ** 2
    # elif val > KB**3:
    else:
        label = "GB"
        val /= KB ** 3
    return str(round(val, 2)) + label