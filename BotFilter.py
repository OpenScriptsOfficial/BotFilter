import datetime
import io
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = 'your API token'  # Replace 'YOUR_API_TOKEN' with your actual bot token
ALLOWED_EXTENSIONS = ['.docx', '.jpg', '.jpeg', '.png', '.gif']  # The allowed file extensions

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['searchfiles'])
async def send_all_files(message: types.Message):
    try:
        files_list = os.listdir("files")
        if files_list:
            files_string = "\n".join(files_list)  # Join the list of files with a line break
            await message.answer("List of files in the directory:\n" + files_string)  # Directly send the list of files
        else:
            await message.answer("The directory does not contain any files")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

async def search_and_send_specific_file(message: Message, file_name: str):
    try:
        file_path = os.path.join("files", file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                await bot.send_document(message.chat.id, file,
                                        caption=file_name)  # Send the document with its name as caption
        else:
            await message.answer(f"The file {file_name} was not found")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@dp.message_handler(commands='sendfile')
async def send_specific_file_command(message: types.Message):
    try:
        # Get the file name from the user's command
        file_name = message.get_args()
        if file_name:
            await search_and_send_specific_file(message, file_name)
        else:
            await message.answer("Please specify the file name in the format:")
            await message.answer("/sendfile file_name")

    except Exception as e:
        await message.answer(f"An error occurred: ```{e}```")

async def save_file(file_bytes, file_name):
    save_dir = 'files'  # Directory for saving files
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Check and create directory if it does not exist
    file_path = os.path.join(save_dir, file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(file_bytes.getbuffer())  # Get byte data from BytesIO object
    return file_path

# Example command to view files
@dp.message_handler(commands=['listfiles'])
async def list_files(message: types.Message):
    try:
        files_list = os.listdir("files")
        if files_list:
            files_string = "\n".join(files_list)
            await message.answer(f"List of files in the directory:\n{files_string}")
        else:
            await message.answer("The directory does not contain any files")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

# Example of deleting a file
@dp.message_handler(commands=['deletefile'])
async def delete_file(message: types.Message):
    try:
        file_name = message.get_args()
        file_path = os.path.join("files", file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            await message.answer(f"The file {file_name} has been deleted")
        else:
            await message.answer(f"The file {file_name} was not found")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

# Example of renaming a file
@dp.message_handler(commands=['renamefile'])
async def rename_file(message: types.Message):
    try:
        args = message.get_args().split()
        if len(args) == 2:
            old_file_name = args[0]
            new_file_name = args[1]
            os.rename(os.path.join("files", old_file_name), os.path.join("files", new_file_name))
            await message.answer(f"The file {old_file_name} has been renamed to {new_file_name}")
        else:
            await message.answer("Please specify the old file name and the new file name")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@dp.message_handler(commands=['deleteallfiles'])
async def delete_all_files_button(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    delete_all_button = types.InlineKeyboardButton(text="Delete All Files", callback_data="confirm_delete_all")
    keyboard.add(delete_all_button)
    await message.answer("Are you sure you want to delete all files in the directory?", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'confirm_delete_all')
async def delete_all_files(callback_query: types.CallbackQuery):
    try:
        files_list = os.listdir("files")
        for file in files_list:
            file_path = os.path.join("files", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        await bot.answer_callback_query(callback_query.id, text="All files have been deleted")
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text=f"An error occurred: {e}")

# Example of creating a subdirectory
@dp.message_handler(commands=['createfolder'])
async def create_folder(message: types.Message):
    try:
        folder_name = message.get_args()
        folder_path = os.path.join("files", folder_name)
        os.makedirs(folder_path)
        await message.answer(f"The folder {folder_name} has been created")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

# Example button for deleting all folders
@dp.message_handler(commands=['deleteallfolders'])
async def delete_all_folders(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Delete all folders", callback_data="delete_all_folders")
    keyboard.add(callback_button)
    await message.answer("Are you sure you want to delete all folders?", reply_markup=keyboard)

# Function to delete all folders
@dp.callback_query_handler(text="delete_all_folders")
async def process_delete_all_folders(callback_query: types.CallbackQuery):
    try:
        folder_path = "files"
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        await callback_query.message.answer("All folders have been deleted")
    except Exception as e:
        await callback_query.message.answer(f"An error occurred: {e}")

async def handle_file_upload(message: types.Message):
    if message.document.file_name.lower().endswith(('.docx', '.jpg', '.jpeg', '.png', '.gif')):
        file_id = message.document.file_id
        file_data = await bot.get_file(file_id)
        file_bytes = await bot.download_file(file_data.file_path)
        file_bytes_io = io.BytesIO(file_bytes)
        file_path = await save_file(file_bytes_io,
                                    file_data.file_path.split('/')[-1])  # Use file name instead of full path
        file_size = os.path.getsize(file_path)
        await register_file(file_data.file_path.split('/')[-1],
                            file_size)  # Register the file using the file name, not the full path

async def register_file(file_name, file_size):
    file_format = file_name.split('.')[-1]
    download_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"File registered - Name: {file_name}, Format: {file_format}, Size: {file_size} bytes, Download Date: {download_date}"
    logging.info(log_message)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    upload_button = types.KeyboardButton("/upload")
    search_button = types.KeyboardButton("/search")
    list_button = types.KeyboardButton("/list")
    delete_button = types.KeyboardButton("/delete")
    rename_button = types.KeyboardButton("/rename")
    create_button = types.KeyboardButton("/create")
    DeleteAllFiles_button = types.KeyboardButton("/deleteallfiles")
    DeleteAllFolders_button = types.KeyboardButton("/deleteallfolders")
    keyboard.add(upload_button, search_button)
    keyboard.add(list_button, delete_button)
    keyboard.add(rename_button, create_button)
    keyboard.add(DeleteAllFiles_button, DeleteAllFolders_button)
    await message.answer("Welcome to the file bot! Please choose an action:", reply_markup=keyboard)

@dp.message_handler(commands=['upload'])
async def upload_file(message: types.Message):
    await message.answer("Please upload the .docx or image file you want to share.")

@dp.message_handler(commands=['search'])
async def search_file(message: types.Message):
    await message.answer("Please specify the file name in the format:")
    await message.answer("/sendfile file_name")

@dp.message_handler(commands=['list'])
async def list_files(message: types.Message):
    # Add a function to retrieve the list of files
    await message.answer("To see a list of files, enter:")
    await message.answer("/searchfiles")

@dp.message_handler(commands=['delete'])
async def delete_file(message: types.Message):
    await message.answer("Please specify the file name in the format:")
    await message.answer("/deletefile file_name")

@dp.message_handler(commands=['rename'])
async def rename_file(message: types.Message):
    await message.answer("Please specify the old file name and the new file name in the format:")
    await message.answer("/renamefile old_file_name new_file_name")

@dp.message_handler(commands=['create'])
async def create_folder(message: types.Message):
    await message.answer("Please specify the folder name in the format:")
    await message.answer("/createfolder folder_name")

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_file_upload(message: types.Message):
    if message.document.file_name.lower().endswith(('.docx', '.jpg', '.jpeg', '.png', '.gif')):
        file_id = message.document.file_id
        file_data = await bot.get_file(file_id)
        downloaded_file = await bot.download_file(file_data.file_path)
        if downloaded_file is not None and file_data.file_path is not None:
            file_path = await save_file(downloaded_file, file_data.file_path.split('/')[-1])  # Saving file using file name, not full path
            if file_path is not None:
                file_size = os.path.getsize(file_path)
                await register_file(file_data.file_path.split('/')[-1], file_size)  # Registering a file using the file name rather than the full path
                await message.answer(f"File uploaded successfully.")
                await message.answer(f"File size: {file_size} bytes.")
                await message.answer(f"File name: {file_data.file_path.split('/')[-1]}")
                await message.answer(f"After uploading the file to the directory, it is advisable to rename the file by entering /rename")
            else:
                await message.answer("Error saving the file.")
        else:
            await message.answer("Error downloading the file.")
    else:
        await message.answer("This file format is not supported for upload, select another file.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
