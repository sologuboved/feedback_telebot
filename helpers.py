import asyncio
from functools import partial, wraps
import logging
import os
import re
import sys
import traceback

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import BadRequest

from userinfo import TOKEN, GROUP_ID


def process_input(update):
    return f"""
<u>From:</u>
id: {update.effective_user.id}
username: {update.effective_user.username}
first name: {update.effective_user.first_name}
last name: {update.effective_user.last_name}

<b><u>Message:</u></b>
{update.message.text}
    """


async def notify(notification, chat_id):
    print(notification)
    notification = f"[<b>Augustblue Feedback</b>]\n{notification}"
    bot = Bot(token=TOKEN)
    async with bot:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=notification,
                parse_mode=ParseMode.HTML,
            )
        except BadRequest:
            await bot.send_message(
                chat_id=chat_id,
                text=notification,
            )


def report_exception(func=None, raise_exception=True):
    if func is None:
        return partial(report_exception, raise_exception=raise_exception)

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            asyncio.run(notify(
                f"({func.__name__}, called with {args}, {kwargs}) {type(e).__name__}: {e}",
                GROUP_ID,
            ))
            if raise_exception:
                raise e
            else:
                traceback_msg = traceback.format_exc()
                logging.error(traceback_msg)

    return wrapper


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname):
    return os.path.join(get_base_dir(), fname)


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = get_abs_path('{}_{}.pid'.format(prefix, str(os.getpid())))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir(get_base_dir()):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return get_abs_path(fname)
