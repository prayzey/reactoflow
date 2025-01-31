# React to Webflow Converter

A web application that converts React code into Webflow-compatible HTML code.

## Features

- Convert React JSX to Webflow-compatible HTML
- Real-time code editing with syntax highlighting
- Easy copy-to-clipboard functionality
- Modern, responsive UI

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Paste your React code in the left editor
2. Click the "Convert" button to transform it to Webflow-compatible code
3. The converted code will appear in the right editor
4. Click the "Copy Result" button to copy the converted code to your clipboard
5. Paste the converted code into Webflow

## Current Conversion Features

- Converts `className` to `class`
- Transforms self-closing tags to standard HTML
- Removes React-specific attributes (onClick, onChange)
- Converts inline styles from React objects to CSS strings
- Basic JSX to HTML conversion

## Note

This is a basic converter and may need additional customization based on specific React features or Webflow requirements.
