"""
In this example, all new messages from the channel <channel> will be persisted in a local database.
All the statistics defined in the `sample_settings.yml` will be printed on the console following the
rules defined in the `.run_callback(response)`.

Parameters:
    <token>: Token for accessing the twitch chat. You can get yours at https://twitchapps.com/tmi/
    <nick>: Nick of the user of the token
    <channel>: Name of the channel to listen
"""

import operator

from twitchchatanalyzer.analyzer.analyzer import Analyzer
from twitchchatanalyzer.twitch_irc import TwitchIRC


def run_callback(response):
    for statistic in response:
        if statistic['type'] == 'HEADER':
            print(statistic['text'])
        if statistic['type'] == 'STATISTIC':
            print(statistic['text'] % tuple(statistic['data_values']))
        if statistic['type'] == 'STATISTIC_RANKING':
            for item in sorted(statistic['data_values'].items(), key=operator.itemgetter(1), reverse=True):
                if item[1] > 0:
                    print(f'{item[0]} - {item[1]}')


analyzer = Analyzer('settings/sample_settings.yml', runnable_callback=run_callback)

tirc = TwitchIRC(server='irc.chat.twitch.tv',
                 port=6667,
                 nick='<nick>',
                 token='<token>',
                 channel='<channel>',
                 callback=Analyzer.persist_callback)

if __name__ == '__main__':
    tirc.start()
    analyzer.start()
