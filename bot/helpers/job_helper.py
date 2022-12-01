from apscheduler.job import Job

from bot.exceptions.telegram_bot_exception import TelegramBotException


def check_job_state(job: Job, module_name: str, must_job_run: bool):
    if job is None:
        raise TelegramBotException(module_name + " is not set in this chat")
    if job.next_run_time and not must_job_run:
        raise TelegramBotException(module_name + " module is already on")
    if job.next_run_time is None and must_job_run:
        raise TelegramBotException(module_name + " module is already off")
