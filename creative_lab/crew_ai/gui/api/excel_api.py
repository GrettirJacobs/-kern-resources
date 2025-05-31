"""
Excel API

This module provides API endpoints for handling Excel file uploads and analysis.
"""

import os
import logging
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from flask import Blueprint, request, jsonify, current_app, render_template
from werkzeug.utils import secure_filename

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the tool framework
try:
    from creative_lab.crew_ai.tools import get_tool_manager
    from creative_lab.crew_ai.tools.document_handlers.excel_handler import ExcelHandler
    TOOLS_AVAILABLE = True
except ImportError:
    logger.error("Tool framework not available.")
    TOOLS_AVAILABLE = False

# Import the memory system
try:
    from creative_lab.crew_ai.memory import get_memory_manager
    MEMORY_AVAILABLE = True
except (ImportError, Exception) as e:
    logger.error(f"Memory system not available: {e}")
    MEMORY_AVAILABLE = False

    # Create a dummy memory manager
    class DummyMemoryManager:
        def store(self, data):
            logger.warning("Using dummy memory manager. Data will not be stored.")
            return "dummy-memory-id"

    def get_memory_manager():
        return DummyMemoryManager()

# Create the blueprint
excel_api = Blueprint('excel_api', __name__)

# Create the upload directory
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'crewai_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Get the real world data directory from environment variables
REAL_WORLD_DATA_DIR = os.environ.get('REAL_WORLD_DATA_DIR', os.path.join(os.path.expanduser('~'), 'kern_resources', 'real_world_data'))
os.makedirs(REAL_WORLD_DATA_DIR, exist_ok=True)

# Create subdirectories
EXCEL_DATA_DIR = os.path.join(REAL_WORLD_DATA_DIR, 'excel_data')
os.makedirs(EXCEL_DATA_DIR, exist_ok=True)

@excel_api.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload an Excel file.

    Returns:
        A JSON response with the upload result
    """
    logger.info("API request: /api/upload")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request files: {request.files}")
    logger.info(f"Request form: {request.form}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request data: {request.data}")

    try:
        # Check if file is in the request
        if 'file' not in request.files:
            logger.error("No file part in the request")
            return jsonify({
                'success': False,
                'error': 'No file part in the request'
            }), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Check file extension
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.xlsx', '.xls', '.csv']:
            return jsonify({
                'success': False,
                'error': 'Invalid file format. Only .xlsx, .xls, and .csv files are allowed.'
            }), 400

        # Save the file to the real world data directory
        file_path = os.path.join(EXCEL_DATA_DIR, filename)
        file.save(file_path)

        # Get sheet names
        if not TOOLS_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Tool framework not available'
            }), 500

        # Get the tool manager
        tool_manager = get_tool_manager()

        # Get the Excel handler
        excel_handler = tool_manager.get_tool('ExcelHandler')
        if not excel_handler:
            # Create the Excel handler
            excel_handler = ExcelHandler()

        # Get sheet names
        result = excel_handler.execute(action='get_sheet_names', file_path=file_path)

        if not result['success']:
            return jsonify({
                'success': False,
                'error': 'Failed to get sheet names'
            }), 500

        return jsonify({
            'success': True,
            'file_path': file_path,
            'sheet_names': result['sheet_names']
        })
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@excel_api.route('/api/analyze', methods=['GET'])
def analyze_file():
    """
    Analyze an Excel file.

    Returns:
        A JSON response with the analysis result
    """
    try:
        # Get parameters
        file_path = request.args.get('file_path')
        sheet_name = request.args.get('sheet_name')

        # Check parameters
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'File path is required'
            }), 400

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404

        # Check if tools are available
        if not TOOLS_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Tool framework not available'
            }), 500

        # Get the tool manager
        tool_manager = get_tool_manager()

        # Get the Excel handler
        excel_handler = tool_manager.get_tool('ExcelHandler')
        if not excel_handler:
            # Create the Excel handler
            excel_handler = ExcelHandler()

        # Analyze the data
        analysis_result = excel_handler.execute(action='analyze_data', file_path=file_path, sheet_name=sheet_name)

        if not analysis_result['success']:
            return jsonify({
                'success': False,
                'error': 'Failed to analyze data'
            }), 500

        # Extract data for preview
        data_result = excel_handler.execute(action='extract_data', file_path=file_path, sheet_name=sheet_name)

        if not data_result['success']:
            return jsonify({
                'success': False,
                'error': 'Failed to extract data'
            }), 500

        # Limit data to 100 rows for preview
        preview_data = data_result['data'][:100]

        # Convert any non-serializable objects to strings
        analysis = analysis_result['analysis']

        return jsonify({
            'success': True,
            'analysis': analysis,
            'data': preview_data
        })
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@excel_api.route('/api/store', methods=['POST'])
def store_in_memory():
    """
    Store Excel data in the memory system.

    Returns:
        A JSON response with the storage result
    """
    try:
        # Get parameters
        file_path = request.args.get('file_path')
        sheet_name = request.args.get('sheet_name')

        # Check parameters
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'File path is required'
            }), 400

        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404

        # Check if tools are available
        if not TOOLS_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Tool framework not available'
            }), 500

        # Check if memory system is available
        if not MEMORY_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Memory system not available'
            }), 500

        # Get the tool manager
        tool_manager = get_tool_manager()

        # Get the Excel handler
        excel_handler = tool_manager.get_tool('ExcelHandler')
        if not excel_handler:
            # Create the Excel handler
            excel_handler = ExcelHandler()

        # Extract data
        data_result = excel_handler.execute(action='extract_data', file_path=file_path, sheet_name=sheet_name)

        if not data_result['success']:
            return jsonify({
                'success': False,
                'error': 'Failed to extract data'
            }), 500

        # Get file info
        file_name = os.path.basename(file_path)

        # Get the memory manager
        memory_manager = get_memory_manager()

        # Store in memory
        memory_id = memory_manager.store({
            'type': 'excel_data',
            'file_name': file_name,
            'sheet_name': sheet_name,
            'data': data_result['data']
        })

        return jsonify({
            'success': True,
            'memory_id': memory_id
        })
    except Exception as e:
        logger.error(f"Error storing in memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def register_excel_api(app):
    """
    Register the Excel API with the Flask app.

    Args:
        app: The Flask app
    """
    app.register_blueprint(excel_api)

    # Upload route is now defined in crewai_gui.py

    logger.info("Excel API registered")
