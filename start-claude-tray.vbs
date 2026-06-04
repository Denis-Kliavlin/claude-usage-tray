Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "pythonw -X utf8 """ & scriptDir & "\claude-usage-tray.py""", 0, False
