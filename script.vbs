 'It would be best if this was not looked at often. 

 Set WshShell = CreateObject("WScript.Shell")
 
 'Kill previous tasks
 WshShell.run "taskkill /f /im python.exe /T", 0, True
 
 'Run
 WshShell.run("scriptingfun\something.sh") 
 WScript.Sleep(100)
 WshShell.run("scriptingfun\something2.sh")
 WScript.Sleep(100)
 WshShell.run("scriptingfun\something3.sh")
 WScript.Sleep(100)

 Set WshShell = Nothing