@echo off
setlocal EnableDelayedExpansion

:: Set the directory to the Desktop of the current user
set "Directory=%USERPROFILE%\Desktop"

:: Initialize the random seed
set /a "random_seed=%random%"

:: Count the number of files in the Desktop directory
set /a "count=0"
for %%F in ("%Directory%\*") do (
    set /a "count+=1"
    set "file[!count!]=%%F"
)

:: Generate a random number between 1 and the count of files
set /a "random_index=(%random_seed% * %count% / 32768) + 1"

:: Open the random file
if %count% GTR 0 (
    start "" "!file[%random_index%]!"
) else (
    echo No files found.
)

endlocal
