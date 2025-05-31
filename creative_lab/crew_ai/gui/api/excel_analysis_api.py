"""
Excel Analysis API

This module provides API endpoints for analyzing Excel files with CrewAI.
"""

import os
import logging
from flask import Blueprint, request, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the Excel analysis workflow
try:
    from creative_lab.crew_ai.excel_analysis_workflow import analyze_and_store_excel
    EXCEL_ANALYSIS_AVAILABLE = True
except ImportError:
    logger.error("Excel analysis workflow not found.")
    EXCEL_ANALYSIS_AVAILABLE = False

# Create the blueprint
excel_analysis_api = Blueprint('excel_analysis_api', __name__)

@excel_analysis_api.route('/api/analyze-excel', methods=['POST'])
def analyze_excel():
    """
    Analyze an Excel file with CrewAI.
    
    Returns:
        A JSON response with the analysis result
    """
    logger.info("API request: /api/analyze-excel")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request data: {request.json}")
    
    try:
        # Check if Excel analysis is available
        if not EXCEL_ANALYSIS_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Excel analysis not available'
            }), 500
        
        # Get parameters
        data = request.json
        file_path = data.get('filePath')
        sheet_name = data.get('sheetName')
        model = data.get('model', 'llama')
        
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
        
        # Analyze the Excel file
        result = analyze_and_store_excel(
            file_path=file_path,
            sheet_name=sheet_name,
            model=model,
            verbose=True
        )
        
        # Return the result
        if result.get('success', False):
            return jsonify({
                'success': True,
                'analysis': result.get('analysis', ''),
                'memory_id': result.get('memory_id', ''),
                'file_path': file_path,
                'sheet_name': sheet_name
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
    except Exception as e:
        logger.error(f"Error analyzing Excel file: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def register_excel_analysis_api(app):
    """
    Register the Excel analysis API with the Flask app.
    
    Args:
        app: The Flask app
    """
    app.register_blueprint(excel_analysis_api)
    logger.info("Excel analysis API registered")
