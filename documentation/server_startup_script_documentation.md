# Memory Search Server Startup Script Documentation

## Overview

The Memory Search Server Startup Script (`start_memory_search_server.ps1`) is a PowerShell script designed to reliably start the Flask server for the Kern Resources memory search application. It includes error handling, dependency checking, and logging to ensure the server starts correctly and any issues are properly documented.

## Features

- **Dependency Checking**: Verifies that Qdrant Docker container is running
- **Environment Validation**: Checks for Python environment and required files
- **Comprehensive Logging**: Logs all actions and errors to a log file
- **Error Handling**: Provides clear error messages and exit codes
- **Browser Integration**: Automatically opens the application in the default browser

## Usage

### Starting the Server

1. **Using PowerShell**:
   ```powershell
   .\start_memory_search_server.ps1
   ```

2. **Using Batch File**:
   - Double-click on `start_server.bat`
   - This will execute the PowerShell script with the appropriate execution policy

### Log Files

The script creates and maintains log files in the `logs` directory:
- `server_startup.log`: Contains startup information, warnings, and errors
- `stdout.log`: Standard output from the Flask server
- `stderr.log`: Standard error output from the Flask server

## Script Workflow

1. **Initialization**:
   - Sets up logging directory and file
   - Defines logging function

2. **Dependency Checks**:
   - Checks if Qdrant Docker container is running
   - Starts Qdrant if it's not running
   - Verifies Python environment status
   - Checks if required files exist

3. **Server Startup**:
   - Starts the Flask server process
   - Monitors the process for successful startup
   - Opens the browser to the application URL
   - Waits for the process to exit or for user interruption

4. **Error Handling**:
   - Logs errors with timestamps and severity levels
   - Provides clear error messages for common issues
   - Exits with appropriate error codes

## Troubleshooting

### Common Issues

1. **Qdrant Not Running**:
   - The script will attempt to start Qdrant automatically
   - If it fails, you may need to start Docker manually

2. **Python Environment Not Activated**:
   - The script will warn if no virtual environment is detected
   - Activate your environment before running the script

3. **Missing Files**:
   - Ensure you're running the script from the correct directory
   - Verify that all required files are present

4. **Port Already in Use**:
   - If port 5001 is already in use, the server will fail to start
   - Check for other processes using the port and terminate them

### Checking Logs

If the server fails to start, check the log files:
```powershell
Get-Content logs\server_startup.log
Get-Content stderr.log
```

## Customization

You can modify the following variables at the top of the script:
- `$LogFile`: Name of the log file
- `$FlaskAppPath`: Path to the Flask application file
- `$Port`: Port number for the Flask server

## Conclusion

The Memory Search Server Startup Script provides a reliable way to start the Flask server for the Kern Resources memory search application. It includes comprehensive error handling and logging to ensure any issues are properly documented and can be easily diagnosed.
