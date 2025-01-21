<-------------------------------------------------------------------------------->

                VARDLL Does not work if it is in python's program folder!!
                Please put VARDLL's Folder within your project for it to work!!

<-------------------------------------------------------------------------------->

How to use:

This example shows how to use vardll 1.4.2:

"from vardll import DLLvar, load_file"

# Load the DLL file
dll_path = 'varotp.dll'
dll_variable = load_file(dll_path)

# Access the variables from the DLL file
print(dll_variable)

Make sure you have the vardll in the directory, like this:

test/
|
|__vardll
|     |
|     |__ __init__.py
|     |__ dllvariable.py
|     |__ license
|     |__ readme.md
|     |__ loader.py
|
|__main.py
|__var0otp.dll

Make sure in var0otp or any dll file you have your variable or the text you wanna input! Disclaimer:

IF THE DLL FILE STAYS EMPTY IT MIGHT MESS UP THE LIBRARY'S CODE!!