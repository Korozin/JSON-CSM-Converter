# JSON-CSM-Converter

This is a Python program I made that converts Blockbench JSON data to CSM / BOX format. For whatever reason people are gate-keeping these tools, so I thought I'd make one. Turns out it was super easy.

## Requirements

-    Python 3.x
-    PyQt5

## How to Use

1.    Run the script using the command `python JSONConvert.py`.
2.    Open your JSON file in a text editor, copy everything (`CTRL + A`), and paste it into the `JSON` Text Box.
3.    Choose the mode you want to convert with by using the provided buttons (EG: `HEAD`, `BODY`, `ARM0` / `ARM1`, etc).
5.    Once you are satisfied with the generated CSM data, click the "Copy" button to copy the data to your clipboard.

## GUI Preview

<img src="https://github.com/Korozin/JSON-CSM-Converter/blob/main/Assets/GUI.png" width="450px" height="600px">

## Classes

This script uses the following classes:

-    MainWindow: The main window of the application.
-    InfoWindow: A window used to display information messages.
-    ErrorWindow: A window used to display error messages.
-    JSONConvert: The main class that handles the logic of the application.

## Credits

This script was created by [KorOwOzin](https://github.com/Korozin). Feel free to use it and modify it as needed. If you find any bugs or issues, please let me know.  

GUI was inspired by [Eden](https://www.youtube.com/@eden3279)

> Licensed under [MIT License](https://github.com/Korozin/JSON-CSM-Converter/blob/main/LICENSE)
