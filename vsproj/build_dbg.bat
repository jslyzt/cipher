@echo off

@call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat"

devenv cipher.sln /Rebuild "Debug|x64"

pause