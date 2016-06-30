# Font width check tool

[Setup]
1. Install Python 2.7.10, don't use 2.7.12.
2. Install xlrd, you can use "pip install xlrd"
3. Copy freetype.dll to C:\Windows\System32\
4. Extract freetype-py-1.0.2.tar.gz
5. Use cmd and change folder to freetype-py-1.0.2, run "python setup.py install"
6. Run script "python TextWidthCheckTool.py > result.txt"
7. Open result.txt to see result.


[Configure]
You can config some parameters in TextWidthCheckTool.py, details see TextWidthCheckTool.py


[Get Result]
1. double click "check_text_width.bat", then open result.txt.
2. double click "get_all_text_width.bat", then open all_text_width.txt to see all text width
