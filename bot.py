from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from helpers import notify, process_input, report_exception, write_pid
from tkn import GROUP_ID, TOKEN


def start(update, context):
    notify(process_input(update), GROUP_ID)
    update.message.reply_text("Ложа, градусъ?")


def send_feedback(update, context):
    notify(process_input(update), GROUP_ID)
    update.message.reply_text('Ευχαριστώ!')


@report_exception
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=send_feedback))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    write_pid()
    main()
