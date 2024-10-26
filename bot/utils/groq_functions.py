import io
from groq import AsyncGroq
from config import settings
from loguru import logger

client = AsyncGroq(
    api_key=settings.GROQ_API_KEY,
)
speech_model = "whisper-large-v3-turbo"
chat_completion_model = "llama-3.2-90b-vision-preview"


async def transcribe_voice(file_io: io.BytesIO) -> str:
    """
    Transcribes an audio file using the Groq API.

    This asynchronous function takes an audio file in binary format and sends it
    to the Groq API for transcription using the specified speech model.
    If successful, it returns the transcribed text in Russian. If an error occurs
    during the API call, it logs the exception and returns an error message.

    Args:
        file_io (io.BytesIO): The audio file in binary format to be transcribed.

    Returns:
        str: The transcribed text if successful, or an error message if an exception occurs.
    """
    logger.info("Send binary-voice file to Groq {model} model", model=speech_model)
    try:
        transcription = await client.audio.transcriptions.create(
            file=("voice.ogg", file_io),
            model=speech_model,
            language="ru",
        )
    except Exception as e:
        logger.exception(f"An error occurred while sending audio to Groq: {str(e)}")
        return "An error occurred while sending audio to Groq"
    logger.info("Get transcription from Groq {model} model", model=speech_model)
    return transcription.text


async def translate_to_english(file_io: io.BytesIO) -> str:
    # logger.info("Send binary-voice file to Groq {model} model", model=speech_model)
    # try:
    #     transcription =  await client.audio.transcriptions.create(
    #             file=("voice.ogg", file_io),
    #             model=speech_model,
    #             language="ru",
    #         )
    # except Exception as e:
    #     logger.exception(f"An error occurred while sending audio to Groq: {str(e)}")
    #     return "An error occurred while sending audio to Groq"
    # logger.info("Get transcription from Groq {model} model", model=speech_model)
    # return transcription.text
    pass


async def chat_completion(text: str) -> str:
    """
    Completes a chat using the Groq API.

    This asynchronous function takes a string of text and sends it to the Groq API
    for chat completion using the specified chat completion model.
    If successful, it returns the completed text. If an error occurs during the API
    call, it logs the exception and returns an error message.

    Args:
        text (str): The text to be completed.

    Returns:
        str: The completed text if successful, or an error message if an exception occurs.
    """
    logger.info(
        "Send text to Groq chat completion {model} model", model=chat_completion_model
    )
    try:
        completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant. If it needed, format content with MARKDOWN",
                },
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
            model=chat_completion_model,
            stream=False,
        )
    except Exception as e:
        logger.exception(f"An error occurred while sending text to Groq: {str(e)}")
        return "An error occurred while sending text to Groq"
    logger.info(
        "Get completion from Groq chat completion {model} model",
        model=chat_completion_model,
    )
    return completion.choices[0].message.content
