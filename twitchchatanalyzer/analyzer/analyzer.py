import operator
from threading import Thread

import time
import yaml

from twitchchatanalyzer.analyzer.database import DB
from twitchchatanalyzer.analyzer.fetcher import messages_with_keys_x_seconds
from twitchchatanalyzer.models import Message as RawMessage
from twitchchatanalyzer.analyzer.models import Message as PersistableMessage


class Analyzer(Thread):
    def __init__(self, settings_file, runnable_callback=None):
        Thread.__init__(self)
        with open(settings_file, 'r') as stream:
            try:
                self.settings = yaml.load(stream)
            except yaml.YAMLError as exp:
                print(exp)

        self.runnable_callback = runnable_callback

        DB.connect()
        for model in [PersistableMessage]:
            if not model.table_exists():
                model.create_table(True)

    @staticmethod
    def persist_callback(message: RawMessage):
        PersistableMessage(username=message.username, text=message.text, time=message.time).save()

    def retrieve_statistics(self):
        response = []

        statistics = self.settings['statistics']
        for statistic in statistics:
            if statistic['type'] == 'HEADER':
                response.append(statistic)
            if statistic['type'] == 'STATISTIC':
                data = []
                for item in statistic['data']:
                    if item['type'] == 'TOTAL':
                        data.append(messages_with_keys_x_seconds(self.settings, item['time'], item['key']))
                    if item['type'] == 'PERCENT':
                        base = messages_with_keys_x_seconds(
                            self.settings,
                            item['data_base']['time'],
                            item['data_base']['key']
                        )
                        relative = messages_with_keys_x_seconds(self.settings, item['time'], item['key'])
                        if base > 0:
                            data.append(round((relative / base) * 100, 2))
                        else:
                            data.append(0)

                statistic['data_values'] = data
                response.append(statistic)
            if statistic['type'] == 'STATISTIC_RANKING':
                data = messages_with_keys_x_seconds(
                    self.settings,
                    statistic['time'],
                    statistic['key'],
                    ranking=True
                )

                statistic['data_value'] = data
                response.append(statistic)

        return response

    def start(self):
        if self.runnable_callback is not None:
            init_time = time.time()
            while True:
                self.runnable_callback(self.retrieve_statistics())

                time.sleep(1 - ((time.time() - init_time) % 1))
            pass
        else:
            raise Exception('To use analyzer as thread, you must set an runnable_callback')
