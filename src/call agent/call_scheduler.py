# src/call_agent/call_scheduler.py


from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()



class CallScheduler:



    def start(self):

        scheduler.start()



    def add_call(
        self,
        function,
        time
    ):


        scheduler.add_job(

            function,

            "date",

            run_date=time

        )