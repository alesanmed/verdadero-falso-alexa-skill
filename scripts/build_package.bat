mkdir ..\upload\

xcopy /s ..\skill\* ..\upload\

call poetry export -f requirements.txt

move ..\requirements.txt ..\upload\requirements.txt

"C:\Program Files\7-Zip\7z.exe" a -tzip "..\upload\lambda.zip" ..\upload\*