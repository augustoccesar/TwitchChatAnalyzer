import time

from peewee import fn

from twitchchatanalyzer.analyzer.models import Message


def messages_with_keys_x_seconds(settings, seconds, keys_key, ranking=False):
    """
    Return the messages count with keys per determinate seconds.

    Positional arguments:
    seconds     --  The number of seconds that the script must look
                    in the past.
    keys_key    --  Name of the key that is on the `twitch.yml` file.
    Keyword arguments:
    ranking     --  If the result should return in form of a ranking, where
                    each key result in a key inside a hash with the value
                    that is the count of occourrences.
    """
    if not keys_key and keys_key not in settings['keys']:
        raise ValueError(
            f'Config file attribute `keys` do not contains `{keys_key}`')

    now = time.time()

    if settings['keys'][keys_key]['meta'].get('no_filter'):
        return Message.select().where(Message.time >= now - seconds).count()
    else:
        if ranking:
            counters = {}
            for key in settings['keys'][keys_key]['list']:
                if settings['keys'][keys_key]['meta']['case'] == 'SENSITIVE':
                    counters[key] = Message.select().where(
                        Message.time >= now - seconds,
                        Message.text.contains(key)
                    ).count()
                elif settings['keys'][keys_key]['meta']['case'] == 'INSENSITIVE':
                    counters[key] = Message.select().where(
                        Message.time >= now - seconds,
                        fn.lower(Message.text).contains(key.lower())
                    ).count()
                else:
                    raise ValueError(
                        'key.meta.case must be "SENSITIVE" or "INSENSITIVE"')

            return counters
        else:
            counter = 0
            for key in settings['keys'][keys_key]['list']:
                if settings['keys'][keys_key]['meta']['case'] == 'SENSITIVE':
                    count = Message.select().where(
                        Message.time >= now - seconds,
                        Message.text.contains(key)
                    ).count()
                    counter += count
                elif settings['keys'][keys_key]['meta']['case'] == 'INSENSITIVE':
                    count = Message.select().where(
                        Message.time >= now - seconds,
                        fn.lower(Message.text).contains(key.lower())
                    ).count()
                    counter += count
                else:
                    raise ValueError(
                        'key.meta.case must be "SENSITIVE" or "INSENSITIVE"')

            return counter
