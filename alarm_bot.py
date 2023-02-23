import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext.jobqueue import Days, Job, JobQueue, Weeks

# Telegram botunuzun token'ını burada belirleyin
TOKEN = "YOUR_TOKEN"

def set_timer(update, context):
    # Kullanıcının gönderdiği süreyi alalım
    timer_time = context.args[0]
    
    # Saat ve dakika değerlerini ayıralım
    timer_time = timer_time.split(":")
    hours, minutes = timer_time
    
    # Şu anki tarihi ve zamanı alalım
    now = datetime.datetime.now()
    
    # Alarmın tarih ve saatini belirleyelim
    alarm_time = now.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
    
    # Şu anki zamanın saat ve dakika değerlerini alalım
    current_time = now.time()
    
    # Eğer alarmın saat ve dakikası şu anki saatten önceyse, alarmın bir sonraki gün olmasını sağlayalım
    if current_time > alarm_time.time():
        alarm_time += datetime.timedelta(days=1)
    
    # Alarmı ayarlayalım
    context.job_queue.run_once(alarm, alarm_time, context=update.message.chat_id)

    update.message.reply_text(f"Alarm {hours}:{minutes} için ayarlandı.")

def alarm(context: CallbackContext):
    # Alarmın çağrıldığı zaman, kullanıcıya bildirim gönderelim
    context.bot.send_message(chat_id=context.job.context, text="Alarm çaldı!")

def main():
    updater = Updater(TOKEN)
    job_queue = JobQueue()
    job_queue.set_dispatcher(updater.dispatcher)
    job_queue.start()

    updater.dispatcher.add_handler(CommandHandler('set_timer', set_timer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
