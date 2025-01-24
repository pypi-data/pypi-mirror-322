"""Cronie is a python library to schedule python functions as cron like jobs, using decorators.

To schedule a async function use::

    from pycronie import cron, run_cron
    @cron("* * * * *")
    async def cron_function():
        pass

    run_cron()

This will register cron_function to be scheduled each minute.
Calling run_cron ensures the cron event loop is executed.

The algorithm used reflects that of unix cron where:

- For each job the next execution time is calculated
- Sleep seconds until the next job(s) is up for execution
- Execute all jobs that are up for execution
- Repeat

"""

from pycronie.cronie import (
    cron,
    reboot,
    startup,
    shutdown,
    minutely,
    hourly,
    midnight,
    daily,
    weekly,
    monthly,
    annually,
    yearly,
    run_cron,
    run_cron_async,
    CronJobInvalid,
    CronJob,
)

__all__ = [
    "cron",
    "reboot",
    "startup",
    "shutdown",
    "minutely",
    "hourly",
    "midnight",
    "daily",
    "weekly",
    "monthly",
    "annually",
    "yearly",
    "run_cron",
    "run_cron_async",
    "CronJobInvalid",
    "CronJob",
]
