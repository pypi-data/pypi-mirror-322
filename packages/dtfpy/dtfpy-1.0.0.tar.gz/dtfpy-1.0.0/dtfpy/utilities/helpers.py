import asyncio
import re
import unicodedata


def create_slug(name: str):
    if not name:
        return None

    # Convert to lowercase and replace spaces with hyphens
    slug = name.lower().replace(' ', '-')

    # Remove any characters that are not letters, numbers, hyphens, or underscores
    slug = re.sub(r'[^a-zA-Z0-9\-_]', '', slug)

    # Normalize the slug to remove any diacritic marks
    slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('utf-8')

    # Remove any leading or trailing hyphens
    slug = slug.strip('-')

    return slug


def safe_access(func, default_value=None):
    try:
        return func()
    except:
        return default_value


def convert_to_int_or_float(string_num):
    try:
        float_num = float(string_num)
        if float_num.is_integer():
            return int(float_num)
        else:
            return float_num
    except ValueError:
        return None


def async_to_sync(awaitable):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)


def chunk_list(lst, chunk_size):
    """Splits a list into chunks of a specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def chunk_list_generator(lst, chunk_size):
    """Generates chunks of a specified size from a list."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
