"""
In this example, all new messages from the channel <channel> will be printed in the screen following the
rule defined in `.callback(message)`.

Parameters:
    <token>: Token for accessing the twitch chat. You can get yours at https://twitchapps.com/tmi/
    <nick>: Nick of the user of the token
    <channel>: Name of the channel to listen
"""

from twitchchatanalyzer.twitch_irc import TwitchIRC


def callback(message):
    print("{}: {}".format(message.username, message.text))


tirc = TwitchIRC(nick='<nick>',
                 token='<token>',
                 channel='<channel>',
                 callback=callback)

if __name__ == '__main__':
    tirc.start()
