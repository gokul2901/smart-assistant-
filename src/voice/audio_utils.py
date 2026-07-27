import os



class AudioUtils:



    SUPPORTED_FORMATS = [

        ".wav",
        ".mp3",
        ".m4a",
        ".ogg"

    ]



    @staticmethod
    def validate_audio(
        file_path
    ):


        extension = os.path.splitext(

            file_path

        )[1].lower()



        return extension in (
            AudioUtils.SUPPORTED_FORMATS
        )



    @staticmethod
    def get_file_size(
        file_path
    ):


        return os.path.getsize(

            file_path

        )



    @staticmethod
    def delete_audio(
        file_path
    ):


        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )