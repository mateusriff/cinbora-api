@ECHO OFF
SETLOCAL

SET "SOURCE_FILE=.github\hooks\pre-commit"
SET "DEST_DIR=.git\hooks"
SET "DEST_FILE=%DEST_DIR%\pre-commit"

IF NOT EXIST "%SOURCE_FILE%" (
    ECHO ERROR: Source file not found at "%SOURCE_FILE%"
    GOTO :EOF
)

IF NOT EXIST "%DEST_DIR%" (
    ECHO ERROR: Git hooks directory not found at "%DEST_DIR%"
    ECHO Make sure you have initialized a git repository.
    GOTO :EOF
)

ECHO Copying %SOURCE_FILE% to %DEST_DIR%...
COPY "%SOURCE_FILE%" "%DEST_FILE%"

IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Failed to copy the file. Please check your permissions.
) ELSE (
    ECHO Successfully copied pre-commit hook.
)

ENDLOCAL
