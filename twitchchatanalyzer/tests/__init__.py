import operator

from twitchchatanalyzer.analyzer.analyzer import Analyzer
from twitchchatanalyzer.twitch_irc import TwitchIRC


def callback(message):
    print('{}: {}'.format(message.username, message.text))


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


analyzer = Analyzer('sample_settings.yml', runnable_callback=run_callback)

tirc = TwitchIRC(server='irc.chat.twitch.tv',
                 port=6667,
                 nick='<your_nick>',
                 token='<your_token>',
                 channel='<channel_name>',
                 callback=Analyzer.persist_callback)

if __name__ == '__main__':
    tirc.start()
    analyzer.start()
