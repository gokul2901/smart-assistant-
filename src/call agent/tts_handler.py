# src/call_agent/tts_handler.py


from kokoro import KPipeline


class TTSHandler:


    def __init__(self):

        self.pipeline = KPipeline(
            lang_code="a"
        )



    async def generate(
        self,
        text,
        output_file
    ):


        audio = self.pipeline(
            text,
            voice="af_heart"
        )


        with open(
            output_file,
            "wb"
        ) as file:

            for _, _, data in audio:

                file.write(data)



        return output_file