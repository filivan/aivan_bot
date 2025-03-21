import io
from groq import AsyncGroq
from config import settings
from loguru import logger

client = AsyncGroq(
    api_key=settings.GROQ_API_KEY,
)


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
    logger.info(
        "Send binary-voice file to Groq {model} model", model=settings.SPEECH_MODEL
    )
    try:
        transcription = await client.audio.transcriptions.create(
            file=("voice.ogg", file_io),
            model=settings.SPEECH_MODEL,
            language="ru",
        )
    except Exception as e:
        logger.exception(f"An error occurred while sending audio to Groq: {str(e)}")
        return "An error occurred while sending audio to Groq"
    logger.info(
        "Get transcription from Groq {model} model", model=settings.SPEECH_MODEL
    )
    return transcription.text


async def chat_completion(text: str, context: str | None = None) -> str:
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
        "Send text to Groq chat completion {model} model",
        model=settings.CHAT_COMPLETION_MODEL,
    )
    if context is not None:
        additional_content = f"The user replied to the message, perhaps he answered something from that message '{context}'"
    try:
        completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant. If it needed, format content with MARKDOWN. "
                    + additional_content
                    if context is not None
                    else "",
                },
                {
                    "role": "user",
                    "content": f"{text}",
                },
            ],
            model=settings.CHAT_COMPLETION_MODEL,
            stream=False,
            temperature=0.6,
            reasoning_format="hidden",
        )
    except Exception as e:
        logger.exception(f"An error occurred while sending text to Groq: {str(e)}")
        return "An error occurred while sending text to Groq"
    logger.info(
        "Get completion from Groq chat completion {model} model",
        model=settings.CHAT_COMPLETION_MODEL,
    )
    return completion.choices[0].message.content


async def image_completion(text: str | None, image_url: str) -> str:
    """
    Completes a chat using the Groq API by sending an image and a text for completion.

    This asynchronous function takes a string of text and an image URL and sends them
    to the Groq API for chat completion using the specified chat completion model.
    If successful, it returns the completed text. If an error occurs during the API
    call, it logs the exception and returns an error message.

    Args:
        text (str): The text to be completed.
        image_url (str): The URL of the image to be completed.

    Returns:
        str: The completed text if successful, or an error message if an exception occurs.
    """
    logger.info(
        "Send image and text to Groq chat completion vision {model} model",
        model=settings.VISION_MODEL,
    )
    try:
        completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            # The text to be completed
                            "type": "text",
                            "text": "What's in this image?" if not text else text,
                        },
                        {
                            # The URL of the image to be completed
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                },
            ],
            model=settings.VISION_MODEL,
            stream=False,
        )
    except Exception as e:
        logger.exception(f"An error occurred while sending text to Groq: {str(e)}")
        return "An error occurred while sending text to Groq"
    logger.info(
        "Get completion from Groq chat completion {model} model",
        model=settings.VISION_MODEL,
    )
    return completion.choices[0].message.content
