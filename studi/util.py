import traceback

def traceback_custom_error():
    lines = traceback.format_exc().split('\n')
    error = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()
    for i in range(0, len(lines) - 1, 2):
        error.append('\t{0} at {1}'.format(lines[i].strip(), lines[i + 1].strip()))
    return '\n'.join(error)