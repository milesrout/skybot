"""
logsql.py: written by milesrout 2017
"""

import os
import codecs
import time
import re
import datetime

from util import hook


VALID_COMMANDS = 'join privmsg pubmsg nick quit action part topic'.upper().split(' ')


def db_init(db):
    db.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    channel, name, time, message, type)''')
    db.commit();


def db_insert(db, input):
    db.execute('''INSERT OR REPLACE INTO messages(channel, name, time, message, type)
                  VALUES(?,?,?,?,?)''',
               (input.chan, input.nick.lower(), datetime.datetime.now(),
                input.msg, input.command))
    db.commit()


@hook.singlethread
@hook.event('*')
def logsql(paraml, db=None, input=None, bot=None):
    if input.command not in VALID_COMMANDS:
        return

    timestamp = datetime.datetime.now()

    if not input.chan:
        input.chan = 'undefined'

    db_init(db)
    db_insert(db, input)


#irc_color_re = re.compile(r'(\x03(\d+,\d+|\d)|[\x0f\x02\x16\x1f])')
