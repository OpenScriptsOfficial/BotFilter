import asyncio
import datetime
import logging
import math
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

# Bot configuration
API_TOKEN = 'YOUR_TOKEN_API'
ALLOWED_EXTENSIONS = {'.docx', '.jpg', '.jpeg', '.png', '.gif'}
SAVE_DIR = 'files'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Helper functions
def get_human_readable_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def register_file(file_name: str, file_size: int) -> None:
    file_format = Path(file_name).suffix[1:]  # Get extension without dot
    download_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"File registered - Name: {file_name}, Format: {file_format}, Size: {file_size} bytes, Download Date: {download_date}"
    logger.info(log_message)


async def save_file(file_bytes: bytes, file_name: str) -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    file_path = os.path.join(SAVE_DIR, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    return file_path


# Keyboard setup
def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="/upload"), KeyboardButton(text="/search")],
            [KeyboardButton(text="/list"), KeyboardButton(text="/delete")],
            [KeyboardButton(text="/rename"), KeyboardButton(text="/create")],
            [KeyboardButton(text="/deleteallfiles"), KeyboardButton(text="/deleteallfolders")]
        ]
    )


# Handlers
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!\nWelcome to the file bot! Please choose an action:",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("upload"))
async def upload_command(message: Message):
    await message.answer("Please upload a .docx or image file (.jpg, .jpeg, .png, .gif).")


@dp.message(Command("search"))
async def search_command(message: Message):
    await message.answer("Please specify the file name using:\n/sendfile <file_name>")


@dp.message(Command("list"))
async def list_command(message: Message):
    await message.answer("To see a list of files, use:\n/searchfiles")


@dp.message(Command("delete"))
async def delete_command(message: Message):
    await message.answer("Please specify the file name using:\n/deletefile <file_name>")


@dp.message(Command("rename"))
async def rename_command(message: Message):
    await message.answer(
        "Please specify the old and new file names using:\n/renamefile <old_file_name> <new_file_name>")


@dp.message(Command("create"))
async def create_command(message: Message):
    await message.answer("Please specify the folder name using:\n/createfolder <folder_name>")


@dp.message(Command("searchfiles"))
async def list_files_command(message: Message):
    try:
        files_list = os.listdir(SAVE_DIR)
        if files_list:
            files_string = "\n".join(files_list)
            await message.answer(f"List of files in the directory:\n{files_string}")
        else:
            await message.answer("The directory does not contain any files.")
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        await message.answer(f"An error occurred: {e}")


@dp.message(Command("sendfile"))
async def send_file_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify the file name using:\n/sendfile <file_name>")
        return
    file_name = args[1]
    try:
        file_path = os.path.join(SAVE_DIR, file_name)
        if os.path.isfile(file_path):
            await message.answer_document(FSInputFile(file_path, filename=file_name))
        else:
            await message.answer(f"The file {file_name} was not found.")
    except Exception as e:
        logger.error(f"Error sending file {file_name}: {e}")
        await message.answer(f"An error occurred: {e}")


@dp.message(Command("deletefile"))
async def delete_file_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify the file name using:\n/deletefile <file_name>")
        return
    file_name = args[1]
    try:
        file_path = os.path.join(SAVE_DIR, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            await message.answer(f"The file {file_name} has been deleted.")
        else:
            await message.answer(f"The file {file_name} was not found.")
    except Exception as e:
        logger.error(f"Error deleting file {file_name}: {e}")
        await message.answer(f"An error occurred: {e}")


@dp.message(Command("renamefile"))
async def rename_file_command(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer(
            "Please specify the old and new file names using:\n/renamefile <old_file_name> <new_file_name>")
        return
    old_file_name, new_file_name = args[1], args[2]
    try:
        old_path = os.path.join(SAVE_DIR, old_file_name)
        new_path = os.path.join(SAVE_DIR, new_file_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            await message.answer(f"The file {old_file_name} has been renamed to {new_file_name}.")
        else:
            await message.answer(f"The file {old_file_name} does not exist.")
    except Exception as e:
        logger.error(f"Error renaming file {old_file_name} to {new_file_name}: {e}")
        await message.answer(f"An error occurred: {e}")


@dp.message(Command("deleteallfiles"))
async def delete_all_files_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Delete All Files", callback_data="confirm_delete_all")]
    ])
    await message.answer("Are you sure you want to delete all files in the directory?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "confirm_delete_all")
async def confirm_delete_all_files(callback: CallbackQuery):
    try:
        files_list = os.listdir(SAVE_DIR)
        for file in files_list:
            file_path = os.path.join(SAVE_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        await callback.message.answer("All files have been deleted.")
        await callback.answer("All files have been deleted.")
    except Exception as e:
        logger.error(f"Error deleting all files: {e}")
        await callback.message.answer(f"An error occurred: {e}")
        await callback.answer(f"An error occurred: {e}")


@dp.message(Command("createfolder"))
async def create_folder_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please specify the folder name using:\n/createfolder <folder_name>")
        return
    folder_name = args[1]
    try:
        folder_path = os.path.join(SAVE_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        await message.answer(f"The folder {folder_name} has been created.")
    except Exception as e:
        logger.error(f"Error creating folder {folder_name}: {e}")
        await message.answer(f"An error occurred: {e}")


@dp.message(Command("deleteallfolders"))
async def delete_all_folders_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Delete All Folders", callback_data="delete_all_folders")]
    ])
    await message.answer("Are you sure you want to delete all folders?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "delete_all_folders")
async def confirm_delete_all_folders(callback: CallbackQuery):
    try:
        for root, dirs, _ in os.walk(SAVE_DIR, topdown=False):
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                    logger.info(f"Deleted folder: {dir_path}")
                except OSError as e:
                    logger.error(f"Error deleting folder {dir_path}: {e}")
        await callback.message.answer("All folders have been deleted.")
        await callback.answer("All folders have been deleted.")
    except Exception as e:
        logger.error(f"Error deleting all folders: {e}")
        await callback.message.answer(f"An error occurred: {e}")
        await callback.answer(f"An error occurred: {e}")


@dp.message(lambda message: message.document)
async def handle_document(message: Message):
    try:
        document = message.document
        if Path(document.file_name).suffix.lower() in ALLOWED_EXTENSIONS:
            file_info = await bot.get_file(document.file_id)
            file_bytes = await bot.download(file_info.file_path)
            file_name = document.file_name
            file_path = await save_file(file_bytes.read(), file_name)
            file_size = os.path.getsize(file_path)

            register_file(file_name, file_size)
            await message.answer(
                f"File '{file_name}' uploaded successfully.\nSize: {get_human_readable_size(file_size)}.\n"
                "Consider renaming the file using /rename."
            )
        else:
            await message.answer("Unsupported file format. Please upload a .docx, .jpg, .jpeg, .png, or .gif file.")
    except Exception as e:
        logger.error(f"Error handling document upload: {e}")
        await message.answer(f"An error occurred: {e}")


# Main function
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
