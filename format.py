
def format_date(dt) -> str:
    return dt.strftime('%Y-%m-%d')


def format_korean(text: str, length: int) -> str:
    postfix = ''
    for ch in text:
        if ch.isascii():
            length -= 1
        else:
            length -= 2
    if length > 0:
        postfix = ' ' * length
    return text + postfix