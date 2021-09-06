@echo off
set baseDir=%CD%
for /D %%i in (*) do (
	if exist %BaseDir%\%%~ni\projCfg.json (
		call :updatePrj %%~ni
	)
)
goto :end

:updatePrj
python tools\updateVsProj.py -p %1 -c %1\projCfg.json -o ./
goto :eof

:end
pause