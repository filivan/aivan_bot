import telegramify_markdown
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from loguru import logger
from filters import MessageToBotFilter
from utils import image_completion


router = Router()

RAW_IMAGE_URL = "https://api.telegram.org/file/bot{bot_token}/{file_path}"


def is_image_mime_type(mime_type: str) -> bool:
    """
    Determine if the given MIME type is for an image.

    Args:
        mime_type (str): The MIME type to check.

    Returns:
        bool: True if the MIME type is for an image, False otherwise.
    """
    return mime_type.startswith("image/")


async def get_image_url(message: Message) -> str | None:
    """
    Retrieve the direct URL for an image from either a photo or document message.

    This function checks if the message contains a photo or a document with an image MIME type,
    and then attempts to obtain the direct file path for the image.

    Args:
        message (Message): The message object containing the photo or document.

    Returns:
        str | None: The file path of the image if found, otherwise None.
    """
    try:
        if message.photo:
            # Get the largest photo size available in the message
            photo = message.photo[-1]
            # Retrieve the file information using the bot's API
            file_info = await message.bot.get_file(photo.file_id)
        elif message.document and is_image_mime_type(message.document.mime_type or ""):
            # Retrieve the file information for the document
            file_info = await message.bot.get_file(message.document.file_id)
        # Return the file path of the image document
        return RAW_IMAGE_URL.format(
            bot_token=message.bot.token, file_path=file_info.file_path
        )
    except Exception as e:
        # Log the error encountered while getting the image URL
        print(f"Error getting image URL: {e}")
        # Return None in case of an exception
        return None


@router.message(F.photo | F.document.mime_type.contains("image/"), MessageToBotFilter())
async def handle_image(message: Message):
    """
    Handle messages containing images (both as photos and documents).

    This function processes incoming messages to extract image URLs and
    sends them for completion using a chat model. The completion result
    is then sent as a reply to the user.

    Args:
        message (Message): The incoming message containing an image.
    """
    try:
        # Get image URL from the message
        image_url = await get_image_url(message)

        # Check if image URL was successfully retrieved
        if not image_url:
            await message.reply("Sorry, I couldn't process this image.")
            return

        if message.caption and message.caption.startswith(
            f"@{message.bot._me.username}"
        ):
            caption = message.caption[len(f"@{message.bot._me.username}") :]
        else:
            caption = message.caption
        # Perform image completion using the retrieved image URL
        completion = await image_completion(caption, image_url)

        # Format the completion result using markdown
        completion = telegramify_markdown.markdownify(completion)

        # Reply to the user with the completion result
        await message.reply(f"{completion}", parse_mode=ParseMode.MARKDOWN_V2)
        logger.info("Completion finished")

    except Exception as e:
        # Handle exceptions and notify the user about the error
        await message.reply(f"An error occurred while processing the image: {str(e)}")
