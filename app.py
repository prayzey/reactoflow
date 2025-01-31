from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app, resources={r"/*": {"origins": "*"}})

# Enable debug logging
logging.getLogger('werkzeug').setLevel(logging.DEBUG)

@app.route('/')
def index():
    logger.info('Serving index.html')
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    logger.info(f'Serving static file: {filename}')
    return send_from_directory(app.static_folder, filename)

def camel_to_kebab(name):
    # Convert camelCase to kebab-case
    name = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', name).lower()

def parse_style_object(style_str):
    # Remove newlines and extra spaces
    style_str = re.sub(r'\s+', ' ', style_str.strip())
    
    # Extract key-value pairs
    style_pairs = []
    current_pair = ''
    brace_count = 0
    quote_char = None
    
    for char in style_str:
        if char in '\'"' and not quote_char:
            quote_char = char
        elif char == quote_char:
            quote_char = None
        elif char == '{' and not quote_char:
            brace_count += 1
        elif char == '}' and not quote_char:
            brace_count -= 1
        elif char == ',' and brace_count == 0 and not quote_char:
            if current_pair.strip():
                style_pairs.append(current_pair.strip())
            current_pair = ''
            continue
        
        current_pair += char
    
    if current_pair.strip():
        style_pairs.append(current_pair.strip())
    
    # Convert each pair to CSS format
    css_pairs = []
    for pair in style_pairs:
        if ':' in pair:
            key, value = pair.split(':', 1)
            key = key.strip().strip('\'"')
            value = value.strip().strip('\'"')
            
            # Convert numeric values
            if value.replace('.', '').isdigit():
                value += 'px'
            
            # Convert camelCase properties to kebab-case
            key = camel_to_kebab(key)
            
            css_pairs.append(f'{key}: {value}')
    
    return '; '.join(css_pairs)

def convert_react_to_webflow(react_code):
    try:
        logger.info('Starting conversion of React code')
        logger.debug(f'Input code:\n{react_code}')
        
        # Remove import statements and exports
        converted_code = re.sub(r'import\s+[^;]+;?\n?', '', react_code)
        converted_code = re.sub(r'export\s+default\s+\w+;?\s*', '', converted_code)
        
        # Remove function declaration and return statement
        converted_code = re.sub(r'function\s+\w+\s*\([^)]*\)\s*{\s*return\s+', '', converted_code)
        
        # Remove closing braces and semicolons
        converted_code = re.sub(r'\s*}\s*;?\s*$', '', converted_code)
        
        # Convert className to class
        converted_code = re.sub(r'className=(["\'])([^"\']*)\1', r'class=\1\2\1', converted_code)
        
        # Handle inline styles with double braces
        def convert_complex_style(match):
            style_content = match.group(1)
            try:
                css_style = parse_style_object(style_content)
                return f'style="{css_style}"'
            except Exception as e:
                logger.error(f'Style conversion error: {e}')
                return match.group(0)
        
        # First handle double-brace styles
        converted_code = re.sub(r'style={{([^}]+)}}', convert_complex_style, converted_code)
        
        # Then handle single-brace styles
        converted_code = re.sub(r'style={["\']([^}"\'])+["\']\}', lambda m: f'style="{m.group(1)}"', converted_code)
        
        # Remove React event handlers
        react_events = ['onClick', 'onChange', 'onSubmit', 'onFocus', 'onBlur', 'onKeyDown', 'onKeyUp', 'onMouseOver', 'onMouseOut']
        for event in react_events:
            converted_code = re.sub(fr'\s+{event}={{[^}}]+}}', '', converted_code)
        
        # Convert self-closing tags
        converted_code = re.sub(r'<([\w-]+)([^>]*?)/>', r'<\1\2></\1>', converted_code)
        
        # Remove JSX expressions (anything in {})
        converted_code = re.sub(r'\{[^}]+\}', '', converted_code)
        
        # Clean up whitespace
        converted_code = re.sub(r'\s+', ' ', converted_code)
        converted_code = re.sub(r'>\s+<', '><', converted_code)
        converted_code = converted_code.strip()
        
        # Remove any remaining curly braces
        converted_code = re.sub(r'[{}]', '', converted_code)
        
        # Remove any remaining 'return' statements
        converted_code = re.sub(r'^\s*return\s+', '', converted_code)
        
        logger.info('Conversion completed successfully')
        logger.debug(f'Output code:\n{converted_code}')
        
        # Format the output nicely
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(converted_code, 'html.parser')
            
            # Get the first div element (the root element)
            root_element = soup.find('div')
            if root_element:
                pretty_html = root_element.prettify()
            else:
                pretty_html = soup.prettify()
            
            # Clean up the prettified HTML
            pretty_html = re.sub(r'\n\s*\n', '\n', pretty_html)  # Remove extra blank lines
            pretty_html = re.sub(r'\s+$', '', pretty_html, flags=re.MULTILINE)  # Remove trailing spaces
            pretty_html = re.sub(r'\s+>', '>', pretty_html)  # Remove space before closing angle bracket
            
            return pretty_html
        except ImportError:
            logger.warning('BeautifulSoup not available for pretty printing')
            return converted_code
        
    except Exception as e:
        logger.error(f'Conversion error: {e}')
        raise Exception(f'Failed to convert React code: {str(e)}')
    except Exception as e:
        print(f'Conversion error: {e}')
        raise Exception(f'Failed to convert React code: {str(e)}')
    
    return converted_code

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    logger.info('=== Received conversion request ===')
    logger.info(f'Request headers: {dict(request.headers)}')
    logger.info(f'Request method: {request.method}')
    try:
        data = request.get_json()
        if not data:
            logger.error('No JSON data received')
            return jsonify({'error': 'No data received'}), 400

        react_code = data.get('code')
        if not react_code:
            logger.error('No code provided in request')
            return jsonify({'error': 'No code provided'}), 400

        logger.debug(f'Received code: {react_code}')
        converted_code = convert_react_to_webflow(react_code)
        logger.debug(f'Converted code: {converted_code}')

        return jsonify({'converted_code': converted_code})
    except Exception as e:
        logger.error(f'Error during conversion: {str(e)}')
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
