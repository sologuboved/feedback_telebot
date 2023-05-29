from telegram.ext import Application, CommandHandler, MessageHandler, filters

from helpers import notify, process_input, report_exception, write_pid
from userinfo import GROUP_ID, TOKEN


async def start(update, context):
    await notify(process_input(update), GROUP_ID)
    await context.bot.send_message(update.message.chat_id, "Ложа, градусъ?")


async def send_feedback(update, context):
    await notify(process_input(update), GROUP_ID)
    await context.bot.send_message(update.message.chat_id, 'Ευχαριστώ!')


@report_exception
def main():
    application = Application.builder().token(token=TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters=filters.TEXT, callback=send_feedback))
    application.run_polling()


if __name__ == '__main__':
    write_pid()
    main()
