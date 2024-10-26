import io
from aiogram import Router, F
from aiogram.types import Message
from loguru import logger
from utils import transcribe_voice

router = Router()


@router.message(F.voice)
async def message_to_voice_with_transcription(message: Message):
    logger.info("Recived voice message from {user_id}", user_id=message.from_user.id)
    # await message.reply("Принял")
    try:
        logger.info("Download voice file")
        # Inform that transcription is in progress
        # processing_msg = await message.reply("Transcribing audio, please wait...")

        # Download the audio file

        io_file: io.BytesIO = await message.bot.download(message.voice.file_id)
        # file = await message.bot.get_file(message.voice.file_id if message.voice else message.audio.file_id)
        # file_path = file.file_path
        # file_name = f"{file.file_id}.ogg"
        # await message.bot.download_file(file_path, file_name)

        # Transcribe the audio
        transcription = await transcribe_voice(io_file)
        # transcript = "transcription"
        # Send the transcription
        await message.reply(f"{transcription}")
        logger.info("Transcription finished")
        # # Delete the processing message
        # await bot.delete_message(chat_id=processing_msg.chat.id, message_id=processing_msg.message_id)

    except Exception:
        logger.exception("An error occurred")
        # await message.reply(f"An error occurred: {str(e)}")

    # finally:
    #     # Clean up the downloaded file
    #     if os.path.exists(file_name):
    #         os.remove(file_name)
