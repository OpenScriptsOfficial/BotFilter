```
$$$$$$$                $$     $$$$$$$$$  $$  $$     $$
$$    $$               $$     $$             $$     $$
$$    $$  $$$$$$$$  $$$$$$$$  $$         $$  $$  $$$$$$$$   $$$$$$   $$ $$$$$
$$$$$$$$  $$    $$     $$     $$$$$$$    $$  $$     $$     $$    $$  $$$ 
$$     $$ $$    $$     $$     $$         $$  $$     $$     $$$$$$$$  $$
$$     $$ $$    $$     $$     $$         $$  $$     $$     $$        $$
$$$$$$$$  $$$$$$$$     $$$$$  $$         $$  4$     $$$$$   $$$$$$$  $$
```

<p align="center"> This bot serves as a versatile tool for managing files in a Telegram environment, combining ease of use with essential file operations, making it suitable for users needing to organize and manipulate files efficiently.  
</p>

## 📝 Overview
<p align="left">
The bot allows users to manage files within a specific directory on the server. Users can upload, delete, rename, and list files, as well as create folders. It supports specific file formats, including .docx .jpg .jpeg .png and .gif.
</p>

## 📑 Key Features
<h3>File Uploading:</h3> Users can upload files in supported formats. The bot saves these files to a designated directory and confirms successful uploads.

<h3>File Listing:</h3>

Users can retrieve a list of all files in the directory using the /searchfiles command.

<h3>File Deletion:</h3>

Users can delete specific files using the /deletefile command or delete all files at once with a confirmation prompt.

<h3>File Renaming:</h3>

The bot allows users to rename files using the /renamefile command, requiring the old and new file names.

<h3>Folder Management:</h3>

Users can create new folders with the /createfolder command and delete all folders through a confirmation process.

<h3>Error Handling:</h3>

The bot includes error handling to inform users of issues such as missing files or unsupported formats.

<h3>Logging:</h3>

The bot logs file uploads, including details like file name, format, size, and upload date, for administrative purposes.

<h3>User Interaction:</h3>

The bot provides a user-friendly interface with command suggestions and inline keyboard options for critical actions, enhancing user experience.

## ⚙ Commands
<span class="command"><u>/start</u> - Initiates the bot and presents the main menu.</span><br>
<span class="command"><u>/upload</u> - Prompts the user to upload a file.</span><br>
<span class="command"><u>/search</u> - Instructs the user on how to search for a specific file.</span><br>
<span class="command"><u>/list</u> - Guides the user to list files.</span><br>
<span class="command"><u>/delete</u> - Instructs on file deletion.</span><br>
<span class="command"><u>/rename</u> - Provides instructions for renaming files.</span><br>
<span class="command"><u>/create</u> - Guides the user to create a folder.</span><br>
<span class="command"><u>/deleteallfiles</u> - Prompts for confirmation to delete all files.</span><br>
<span class="command"><u>/deleteallfolders</u> - Prompts for confirmation to delete all folders.</span><br>
