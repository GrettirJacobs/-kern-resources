"""
Simple Excel Analysis API

This module provides API endpoints for analyzing Excel files without using CrewAI or the memory system.
"""

import os
import logging
import json
from flask import Blueprint, request, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the simple Excel analysis
try:
    from creative_lab.crew_ai.gui.simple_excel_analysis import analyze_excel_file
    EXCEL_ANALYSIS_AVAILABLE = True
except ImportError:
    logger.error("Simple Excel analysis not found.")
    EXCEL_ANALYSIS_AVAILABLE = False

# Create the blueprint
simple_excel_api = Blueprint('simple_excel_api', __name__)

@simple_excel_api.route('/api/simple-analyze-excel', methods=['POST'])
def analyze_excel():
    """
    Analyze an Excel file without using CrewAI or the memory system.
    
    Returns:
        A JSON response with the analysis result
    """
    logger.info("API request: /api/simple-analyze-excel")
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
        result = analyze_excel_file(
            file_path=file_path,
            sheet_name=sheet_name
        )
        
        # Return the result
        if result.get('success', False):
            # Convert the analysis to a formatted string for display
            analysis = result.get('analysis', {})
            analysis_text = format_analysis_for_display(analysis)
            
            return jsonify({
                'success': True,
                'analysis': analysis_text,
                'raw_analysis': analysis,
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

def format_analysis_for_display(analysis: dict) -> str:
    """
    Format the analysis results for display.
    
    Args:
        analysis: The analysis results
        
    Returns:
        A formatted string for display
    """
    file_path = analysis.get('file_path', 'Unknown')
    sheet_name = analysis.get('sheet_name', 'Default')
    num_rows = analysis.get('num_rows', 0)
    num_columns = analysis.get('num_columns', 0)
    columns = analysis.get('columns', [])
    column_stats = analysis.get('column_stats', {})
    sample_data = analysis.get('sample_data', [])
    
    # Create the formatted string
    text = f"# Excel File Analysis\n\n"
    text += f"## File Information\n"
    text += f"- **File Path:** {file_path}\n"
    text += f"- **Sheet Name:** {sheet_name}\n"
    text += f"- **Number of Rows:** {num_rows}\n"
    text += f"- **Number of Columns:** {num_columns}\n\n"
    
    text += f"## Column Information\n"
    for column in columns:
        stats = column_stats.get(column, {})
        text += f"### {column}\n"
        text += f"- **Type:** {stats.get('type', 'Unknown')}\n"
        text += f"- **Null Count:** {stats.get('null_count', 0)}\n"
        text += f"- **Unique Count:** {stats.get('unique_count', 0)}\n"
        
        if 'min' in stats:
            text += f"- **Min:** {stats.get('min')}\n"
            text += f"- **Max:** {stats.get('max')}\n"
            text += f"- **Mean:** {stats.get('mean')}\n"
            text += f"- **Median:** {stats.get('median')}\n"
            text += f"- **Standard Deviation:** {stats.get('std')}\n"
        
        if 'most_common' in stats:
            text += f"- **Most Common Values:**\n"
            for value, count in stats.get('most_common', {}).items():
                text += f"  - {value}: {count}\n"
        
        text += "\n"
    
    text += f"## Sample Data (First {len(sample_data)} Rows)\n"
    if sample_data:
        # Create a table header
        text += "| " + " | ".join(columns) + " |\n"
        text += "| " + " | ".join(["---"] * len(columns)) + " |\n"
        
        # Add the data rows
        for row in sample_data:
            text += "| " + " | ".join([str(row.get(col, '')) for col in columns]) + " |\n"
    else:
        text += "No data available.\n"
    
    return text

def register_simple_excel_api(app):
    """
    Register the simple Excel analysis API with the Flask app.
    
    Args:
        app: The Flask app
    """
    app.register_blueprint(simple_excel_api)
    logger.info("Simple Excel analysis API registered")
