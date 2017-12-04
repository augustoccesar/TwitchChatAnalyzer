> Author: Augusto César Freitas e Silva
>
> Email: augusto.acfs@gmail.com

# Twitch Chat Analyzer
Tools for analyzing twitch chat.

## Dependencies
- **PyYaml** - For managing the .yml config file.
- **Peewee** - For database.

## The settings yaml file to analyze
This file contains configuration that is used to run the script. This file contains the following attributes:
- **keys** - The keys to be looking on messages to generate data.
- **statistics** - Statistics definitions.

## Keys Structure
The keys are structured in a way that a modification on the `.yml` file can open the possibilities of data to extract. It consists of the following attributes:
- **meta** - Meta data that is analysed when parsing.
    - **no_filter** - When this attribute is defined, the search will disconsider the `list` attribute (since it is looking for all).
    - **case** - It can be `INSENSITIVE` or `SENSITIVE` for knowing how to look for the string inside the `list` attribute.
- **list** - The list of strings that will be searched on the messages.


## Statistics Structure
The statistic objects in the yml file are divided in types.

### Type Header
The type `HEADER` contains two attributes:
- **type** - The type defined `HEADER` to be recognized as so by the code.
- **text** - The text that will be displayed by the `.show()` method.

*Example:*
```yaml
type: HEADER
text: ------------ Messages Stats -------------
```

### Type Statistic
The type `STATISTIC` contains four attributes:
- **type** - The type defined `STATISTIC` to be recognized as so by the code.
- **name** - The name of the statistic (for organization and readbility).
- **text** - The text markedown with `%s` or `%i` or `%f` to be replaced by order by the items inside `data` attribute.
- **data** - Contains the data that will be inserted in the `text`.
    - **type** - Type of the data. Can be `TOTAL` or `PERCENT`. When `TOTAL` it will fetch the sum of messages that contains `key` on it. When `PERCENT` (it requires a `data_base`) it will divide the result of the self data by the result of the `data_base`.
    - **key** - The `key` in `keys` at the settings yaml file that will be searched on the messages.
    - **time** - The time range of the messages in seconds. `60` means: `from 60 seconds ago until now`.
    - **data_base** - The base of the percentage
        - **key** - The `key` in `keys` at the settings yaml file that will be searched on the messages.
        - **time** - The time range of the messages in seconds. `60` means: `from 60 seconds ago until now`.

*Examples:*
```yaml
- type: STATISTIC
    name: 'Troll messages per minute + percentage'
    text: '%i troll messages/minute (%.2f%%)'
    data:
      - type: TOTAL
        key: troll
        time: 60
      - type: PERCENT
        data_base:
          key: all
          time: 60
        key: troll
        time: 60
```
```yaml
- type: STATISTIC
    name: 'Total messages per second'
    text: '%i messages/second'
    data:
      - type: TOTAL
        key: all
        time: 1
```

### Type Statistic Ranking
The type `STATISTIC_RANKING` contains four attributes:
- **type** - The type defined `STATISTIC_RANKING` to be recognized as so by the code.
- **name** - The name of the statistic (for organization and readbility).
- **text** - The text markedown with `%s` or `%i` or `%f` to be replaced by order by the items inside `data` attribute.
- **key** - The `key` in `keys` at the settings yaml file that will be searched on the messages to be in the ranking.
- **time** - The time range of the messages in seconds. `60` means: `from 60 seconds ago until now`.

*Example:*
```yaml
- type: STATISTIC_RANKING
    name: 'Emotes ranking per minute'
    text: '%s - %i'
    key: emote
    time: 60
```