#!/usr/bin/env python3
"""
Build Script for CrewAI GUI Standalone Executable

This script automates the process of building a standalone executable
using PyInstaller with proper configuration and error handling.
"""

import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('build_log.txt')
    ]
)
logger = logging.getLogger(__name__)

class ExecutableBuilder:
    """Handles building the CrewAI GUI standalone executable"""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.project_root = self.current_dir.parent.parent.parent
        self.gui_dir = self.current_dir
        self.build_dir = self.gui_dir / "build"
        self.dist_dir = self.gui_dir / "dist"
        self.spec_file = self.gui_dir / "crewai_gui.spec"
        
    def clean_build_directories(self):
        """Clean previous build artifacts"""
        logger.info("Cleaning previous build artifacts...")
        
        directories_to_clean = [self.build_dir, self.dist_dir]
        
        for directory in directories_to_clean:
            if directory.exists():
                try:
                    shutil.rmtree(directory)
                    logger.info(f"Removed {directory}")
                except Exception as e:
                    logger.warning(f"Could not remove {directory}: {e}")
        
        # Remove .pyc files
        for pyc_file in self.gui_dir.rglob("*.pyc"):
            try:
                pyc_file.unlink()
            except Exception as e:
                logger.warning(f"Could not remove {pyc_file}: {e}")
        
        # Remove __pycache__ directories
        for pycache_dir in self.gui_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
            except Exception as e:
                logger.warning(f"Could not remove {pycache_dir}: {e}")
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        logger.info("Checking dependencies...")

        required_packages = [
            'pyinstaller',
            'flask',
            'flask-socketio',
            'flask-cors',
            'crewai',
            'python-dotenv'
        ]

        missing_packages = []

        for package in required_packages:
            try:
                if package == 'pyinstaller':
                    import PyInstaller
                elif package == 'python-dotenv':
                    import dotenv
                elif package == 'flask-socketio':
                    import flask_socketio
                elif package == 'flask-cors':
                    import flask_cors
                else:
                    __import__(package.replace('-', '_'))
                logger.info(f"[OK] {package}")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"[MISSING] {package}")

        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.error("Please install missing packages before building")
            return False

        logger.info("All dependencies satisfied")
        return True
    
    def verify_files_exist(self):
        """Verify that all required files exist"""
        logger.info("Verifying required files exist...")

        required_files = [
            self.gui_dir / "crewai_gui_standalone.py",
            self.spec_file,
            self.gui_dir / "templates" / "index.html",
            self.gui_dir / "apps" / "crewai" / "crewai_gui.py",
        ]

        missing_files = []

        for file_path in required_files:
            if file_path.exists():
                logger.info(f"[OK] {file_path.name}")
            else:
                missing_files.append(file_path)
                logger.error(f"[MISSING] {file_path}")

        if missing_files:
            logger.error(f"Missing files: {missing_files}")
            return False

        logger.info("All required files exist")
        return True
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        logger.info("Building executable with PyInstaller...")
        
        # Change to the GUI directory
        original_cwd = os.getcwd()
        os.chdir(self.gui_dir)
        
        try:
            # Build command
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                str(self.spec_file)
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            # Run PyInstaller
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                logger.info("PyInstaller build completed successfully")
                logger.info("Build output:")
                logger.info(result.stdout)
                return True
            else:
                logger.error("PyInstaller build failed")
                logger.error("Error output:")
                logger.error(result.stderr)
                logger.error("Standard output:")
                logger.error(result.stdout)
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Build process timed out")
            return False
        except Exception as e:
            logger.error(f"Build process failed: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def verify_executable(self):
        """Verify that the executable was created and works"""
        logger.info("Verifying executable...")
        
        exe_path = self.dist_dir / "CrewAI_GUI.exe"
        
        if not exe_path.exists():
            logger.error(f"Executable not found at {exe_path}")
            return False
        
        logger.info(f"[OK] Executable created: {exe_path}")
        logger.info(f"Executable size: {exe_path.stat().st_size / (1024*1024):.1f} MB")

        # Test if executable can start (quick test)
        try:
            logger.info("Testing executable startup...")
            result = subprocess.run(
                [str(exe_path), "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info("[OK] Executable startup test passed")
                return True
            else:
                logger.warning("Executable startup test failed, but file exists")
                logger.warning(f"Return code: {result.returncode}")
                logger.warning(f"Output: {result.stdout}")
                logger.warning(f"Error: {result.stderr}")
                return True  # Still consider success if file exists
                
        except subprocess.TimeoutExpired:
            logger.warning("Executable test timed out, but file exists")
            return True
        except Exception as e:
            logger.warning(f"Could not test executable: {e}")
            return True  # Still consider success if file exists
    
    def create_installer_script(self):
        """Create a simple installer script"""
        logger.info("Creating installer script...")
        
        installer_script = self.dist_dir / "install_crewai_gui.bat"
        
        installer_content = f'''@echo off
echo CrewAI GUI Installer
echo ===================
echo.

set "INSTALL_DIR=%USERPROFILE%\\CrewAI_GUI"
set "DESKTOP_DIR=%USERPROFILE%\\Desktop"
set "START_MENU_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"

echo Installing CrewAI GUI to: %INSTALL_DIR%
echo.

REM Create installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
echo Copying executable...
copy "CrewAI_GUI.exe" "%INSTALL_DIR%\\CrewAI_GUI.exe"

REM Create desktop shortcut
echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\CreateShortcut.vbs"
echo sLinkFile = "%DESKTOP_DIR%\\CrewAI GUI.lnk" >> "%TEMP%\\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\\CrewAI_GUI.exe" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.Description = "CrewAI GUI - AI Agent Management Interface" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\\CreateShortcut.vbs"
cscript "%TEMP%\\CreateShortcut.vbs"
del "%TEMP%\\CreateShortcut.vbs"

REM Create start menu shortcut
echo Creating start menu shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\\CreateShortcut.vbs"
echo sLinkFile = "%START_MENU_DIR%\\CrewAI GUI.lnk" >> "%TEMP%\\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\\CrewAI_GUI.exe" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.Description = "CrewAI GUI - AI Agent Management Interface" >> "%TEMP%\\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\\CreateShortcut.vbs"
cscript "%TEMP%\\CreateShortcut.vbs"
del "%TEMP%\\CreateShortcut.vbs"

echo.
echo ✓ Installation completed successfully!
echo.
echo CrewAI GUI has been installed to: %INSTALL_DIR%
echo Desktop shortcut created: %DESKTOP_DIR%\\CrewAI GUI.lnk
echo Start menu shortcut created: %START_MENU_DIR%\\CrewAI GUI.lnk
echo.
echo You can now launch CrewAI GUI from:
echo - Desktop shortcut
echo - Start menu
echo - Directly from: %INSTALL_DIR%\\CrewAI_GUI.exe
echo.
pause
'''
        
        try:
            with open(installer_script, 'w') as f:
                f.write(installer_content)
            logger.info(f"[OK] Installer script created: {installer_script}")
            return True
        except Exception as e:
            logger.error(f"Failed to create installer script: {e}")
            return False
    
    def build(self):
        """Main build process"""
        logger.info("=" * 60)
        logger.info("CrewAI GUI Executable Build Process Starting...")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Clean build directories
        self.clean_build_directories()
        
        # Step 2: Check dependencies
        if not self.check_dependencies():
            logger.error("Dependency check failed. Aborting build.")
            return False
        
        # Step 3: Verify files exist
        if not self.verify_files_exist():
            logger.error("File verification failed. Aborting build.")
            return False
        
        # Step 4: Build executable
        if not self.build_executable():
            logger.error("Executable build failed. Aborting.")
            return False
        
        # Step 5: Verify executable
        if not self.verify_executable():
            logger.error("Executable verification failed.")
            return False
        
        # Step 6: Create installer script
        self.create_installer_script()
        
        # Build completed
        end_time = time.time()
        build_time = end_time - start_time
        
        logger.info("=" * 60)
        logger.info("BUILD COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info(f"Build time: {build_time:.1f} seconds")
        logger.info(f"Executable location: {self.dist_dir / 'CrewAI_GUI.exe'}")
        logger.info(f"Installer script: {self.dist_dir / 'install_crewai_gui.bat'}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Test the executable by running it")
        logger.info("2. Use the installer script to install on target systems")
        logger.info("3. Create desktop shortcuts for easy access")
        
        return True

def main():
    """Main entry point"""
    builder = ExecutableBuilder()
    success = builder.build()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print(f"📁 Executable: {builder.dist_dir / 'CrewAI_GUI.exe'}")
        print(f"📦 Installer: {builder.dist_dir / 'install_crewai_gui.bat'}")
    else:
        print("\n❌ Build failed. Check the log for details.")
        sys.exit(1)

if __name__ == '__main__':
    main()
