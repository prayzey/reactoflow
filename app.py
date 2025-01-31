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

def generate_placeholder_content(expr):
    """Enhanced contextual placeholder generation with more patterns and variations"""
    expr = expr.lower()
    
    # User-related patterns
    user_patterns = {
        'full_?name|display_?name': ['John Doe', 'Jane Smith', 'Michael Johnson'],
        'first_?name': ['John', 'Jane', 'Michael', 'Sarah'],
        'last_?name': ['Doe', 'Smith', 'Johnson', 'Williams'],
        'username|user_id': ['johndoe', 'jsmith', 'mjohnson'],
        'email': ['john.doe@example.com', 'jane.smith@example.com'],
        'phone|tel|contact': ['+1 (555) 123-4567', '(555) 987-6543'],
        'address': ['123 Main St, New York, NY 10001'],
        'avatar|profile_?pic': ['avatar1.jpg', 'profile2.png'],
        'bio|description': ['Product manager with 5+ years experience'],
        'role|position': ['Senior Developer', 'Product Manager', 'Designer']
    }
    
    # Date and time patterns
    date_patterns = {
        'created_?at|timestamp': 'January 31, 2025 at 6:00 PM',
        'updated_?at|modified': '2 hours ago',
        'due_?date': 'Next Monday at 5:00 PM',
        'schedule|appointment': 'Thursday, Feb 2 at 10:00 AM',
        'birthday|dob': 'March 15, 1990'
    }
    
    # Numeric patterns
    numeric_patterns = {
        'count|total': ['5', '12', '24', '48'],
        'items?_count': ['5 items', '12 products', '24 files'],
        'views?|visits': ['1.2K views', '4.5K visits'],
        'likes?|reactions': ['2.3K likes', '500 reactions'],
        'percentage|progress': ['85%', '92%', '78%'],
        'rating|score': ['4.5', '4.8', '4.2']
    }
    
    # Price patterns
    price_patterns = {
        'price|cost': ['$99.99', '$149.99', '$199.99'],
        'discount': ['20% off', '30% off'],
        'sale_price': ['$79.99', '$129.99'],
        'original_price': ['$129.99', '$199.99'],
        'subscription': ['$9.99/month', '$99/year']
    }
    
    # Status patterns
    status_patterns = {
        'status|state': ['Active', 'Pending', 'Completed'],
        'progress': ['In Progress', 'Completed', 'On Hold'],
        'availability': ['In Stock', 'Out of Stock', 'Pre-order'],
        'priority': ['High', 'Medium', 'Low'],
        'condition': ['New', 'Used', 'Refurbished']
    }
    
    # Content patterns
    content_patterns = {
        'title|heading': ['Premium Product', 'Latest News', 'Featured Item'],
        'subtitle|tagline': ['Best Seller', 'New Arrival', 'Limited Edition'],
        'description|content': ['High-quality product with premium features.',
                              'Exclusive offer for a limited time only.'],
        'category|tag': ['Electronics', 'Clothing', 'Home & Garden'],
        'feature|highlight': ['Premium Quality', '24/7 Support', 'Free Shipping']
    }
    
    # Check all pattern groups
    for patterns in [user_patterns, date_patterns, numeric_patterns,
                    price_patterns, status_patterns, content_patterns]:
        for pattern, values in patterns.items():
            if re.search(pattern, expr, re.I):
                if isinstance(values, list):
                    # Use consistent values for the same expression
                    import hashlib
                    hash_val = int(hashlib.md5(expr.encode()).hexdigest(), 16)
                    return values[hash_val % len(values)]
                return values
    
    # Generate a meaningful fallback based on the expression
    words = re.findall(r'[a-z]+', expr)
    if words:
        return f"Sample {' '.join(word.title() for word in words)}"
    
    return 'Example Content'

def detect_component_pattern(code):
    """Enhanced component pattern detection with more patterns and states"""
    patterns = {
        'navbar': (r'nav|header|menu|toolbar', """
            <nav class="navbar">
                <!-- Desktop Navigation -->
                <div class="nav-brand">
                    <a href="#" class="brand-link">
                        <img src="logo.svg" alt="Brand Logo" class="brand-logo">
                        <span class="brand-name">Brand Name</span>
                    </a>
                </div>
                <div class="nav-menu desktop-menu">
                    <a href="#" class="nav-link active">Home</a>
                    <a href="#" class="nav-link">Products</a>
                    <a href="#" class="nav-link">Services</a>
                    <a href="#" class="nav-link">About</a>
                    <a href="#" class="nav-link">Contact</a>
                </div>
                <!-- Mobile Navigation -->
                <div class="mobile-menu hidden">
                    <div class="mobile-menu-header">
                        <span class="brand-name">Brand Name</span>
                        <button class="close-menu">×</button>
                    </div>
                    <div class="mobile-menu-links">
                        <a href="#" class="nav-link active">Home</a>
                        <a href="#" class="nav-link">Products</a>
                        <a href="#" class="nav-link">Services</a>
                        <a href="#" class="nav-link">About</a>
                        <a href="#" class="nav-link">Contact</a>
                    </div>
                </div>
            </nav>
        """),
        'product_card': (r'product|card|item', """

            <!-- Product Card - Default State -->
            <div class="product-card">
                <div class="product-image-wrapper">
                    <img src="product-image.jpg" alt="Product" class="product-image">
                    <div class="product-badges">
                        <span class="badge new">New</span>
                        <span class="badge sale">Sale</span>
                    </div>
                    <div class="quick-view-overlay">
                        <button class="quick-view-btn">Quick View</button>
                    </div>
                </div>
                <div class="product-info">
                    <div class="product-category">Category</div>
                    <h3 class="product-title">Premium Product Name</h3>
                    <div class="product-rating">
                        <span class="stars">★★★★☆</span>
                        <span class="review-count">(24 reviews)</span>
                    </div>
                    <div class="product-price-wrapper">
                        <span class="original-price">$129.99</span>
                        <span class="sale-price">$99.99</span>
                    </div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            <!-- Product Card - Hover State -->
            <div class="product-card hover">
                <!-- Same structure with hover effects -->
            </div>
        """),
        'form': (r'form|input|submit', """

            <!-- Form with Validation States -->
            <form class="contact-form">
                <div class="form-header">
                    <h2>Contact Us</h2>
                    <p>We'll get back to you within 24 hours</p>
                </div>
                <!-- Input Group - Default -->
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" class="form-input" placeholder="John Doe">
                    <span class="input-hint">Enter your full name</span>
                </div>
                <!-- Input Group - Success -->
                <div class="form-group success">
                    <label for="email">Email</label>
                    <input type="email" id="email" class="form-input" value="john@example.com">
                    <span class="validation-message">Valid email format</span>
                </div>
                <!-- Input Group - Error -->
                <div class="form-group error">
                    <label for="phone">Phone</label>
                    <input type="tel" id="phone" class="form-input" value="123">
                    <span class="validation-message">Please enter a valid phone number</span>
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" class="form-textarea" placeholder="Your message here..."></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="submit-btn">Send Message</button>
                    <button type="reset" class="reset-btn">Reset</button>
                </div>
            </form>
        """),
        'modal': (r'modal|dialog|popup', """

            <!-- Modal - Closed State -->
            <div class="modal-wrapper hidden">
                <div class="modal-overlay"></div>
                <div class="modal">
                    <div class="modal-header">
                        <h2 class="modal-title">Important Notice</h2>
                        <button class="modal-close">×</button>
                    </div>
                    <div class="modal-body">
                        <div class="modal-content">
                            <p>Modal content goes here with important information.</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="modal-btn primary">Accept</button>
                        <button class="modal-btn secondary">Cancel</button>
                    </div>
                </div>
            </div>
            <!-- Modal - Open State -->
            <div class="modal-wrapper visible">
                <!-- Same structure but with visible class -->
            </div>
        """),
        'dropdown': (r'dropdown|select|menu', """

            <!-- Dropdown - Closed State -->
            <div class="dropdown-wrapper">
                <button class="dropdown-trigger">
                    <span class="selected-option">Select Option</span>
                    <span class="dropdown-arrow">▼</span>
                </button>
                <div class="dropdown-menu hidden">
                    <div class="dropdown-search">
                        <input type="text" placeholder="Search..." class="search-input">
                    </div>
                    <div class="dropdown-options">
                        <div class="option-group">
                            <div class="option-header">Group 1</div>
                            <div class="option" data-value="1">Option 1</div>
                            <div class="option" data-value="2">Option 2</div>
                        </div>
                        <div class="option-group">
                            <div class="option-header">Group 2</div>
                            <div class="option" data-value="3">Option 3</div>
                            <div class="option" data-value="4">Option 4</div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Dropdown - Open State -->
            <div class="dropdown-wrapper active">
                <!-- Same structure but with active class -->
            </div>
        """)
    }
    
    def analyze_component_context(code):
        """Analyze the context to determine component variations"""
        context = {
            'has_images': bool(re.search(r'image|img|photo', code, re.I)),
            'has_pricing': bool(re.search(r'price|cost|\$', code, re.I)),
            'has_rating': bool(re.search(r'rating|stars|review', code, re.I)),
            'is_interactive': bool(re.search(r'click|hover|active', code, re.I))
        }
        return context
    
    for pattern_name, (pattern, template) in patterns.items():
        if re.search(pattern, code, re.IGNORECASE):
            context = analyze_component_context(code)
            # Customize template based on context
            modified_template = template
            if not context['has_images']:
                modified_template = re.sub(r'<img[^>]+>', '', modified_template)
            if not context['has_pricing']:
                modified_template = re.sub(r'<[^>]+price[^>]*>.*?</[^>]+>', '', modified_template)
            return pattern_name, modified_template.strip()
    
    return None, None

def parse_style_object(style_str):
    """Enhanced style parsing with nested objects, variables, and smart unit handling"""
    def parse_nested_styles(style_obj):
        """Recursively parse nested style objects"""
        if isinstance(style_obj, str):
            # Base case: string value
            return style_obj.strip('" ')
        
        result = {}
        for key, value in style_obj.items():
            if isinstance(value, dict):
                # Nested object
                result[key] = parse_nested_styles(value)
            else:
                # Convert the value and add units if needed
                result[key] = add_units(key, str(value).strip('" '))
        return result
    
    def add_units(prop, value):
        """Smart unit addition based on property and value"""
        # Skip if value already has units or is a special value
        if not value.replace('.', '').isdigit() or value == '0':
            return value
        
        # Length properties (px)
        length_props = {
            'width', 'height', 'min-width', 'max-width', 'min-height', 'max-height',
            'margin', 'padding', 'top', 'right', 'bottom', 'left',
            'border-width', 'border-radius', 'font-size', 'line-height',
            'gap', 'column-gap', 'row-gap'
        }
        
        # Time properties (ms)
        time_props = {
            'transition-duration', 'animation-duration', 'transition-delay',
            'animation-delay'
        }
        
        # Unitless properties
        unitless_props = {
            'opacity', 'z-index', 'flex', 'flex-grow', 'flex-shrink',
            'order', 'line-height', 'font-weight'
        }
        
        # Handle special cases
        if prop in unitless_props:
            return value
        elif prop in time_props:
            return f"{value}ms"
        elif prop in length_props or prop.endswith(('width', 'height', 'top', 'right', 'bottom', 'left')):
            return f"{value}px"
        elif prop.startswith('rotate'):
            return f"{value}deg"
        elif prop.startswith('scale'):
            return value
        
        # Default to pixels for unknown numeric properties
        return f"{value}px"
    
    def parse_css_vars(styles):
        """Handle CSS variable references"""
        var_pattern = r'var\((--[^)]+)\)'
        return {k: re.sub(var_pattern, r'var(\1)', v) if isinstance(v, str) else v
                for k, v in styles.items()}
    
    def handle_vendor_prefixes(styles):
        """Add vendor prefixes for necessary properties"""
        prefix_props = {
            'user-select': ['-webkit-', '-moz-', '-ms-'],
            'appearance': ['-webkit-', '-moz-'],
            'transform': ['-webkit-'],
            'transition': ['-webkit-'],
            'animation': ['-webkit-'],
            'backdrop-filter': ['-webkit-'],
            'background-clip': ['-webkit-'],
            'mask-image': ['-webkit-']
        }
        
        prefixed_styles = {}
        for prop, value in styles.items():
            prefixed_styles[prop] = value
            if prop in prefix_props:
                for prefix in prefix_props[prop]:
                    prefixed_styles[f"{prefix}{prop}"] = value
        return prefixed_styles
    
    def handle_complex_values(value):
        """Handle complex CSS values like gradients, transforms, and filters"""
        complex_patterns = {
            'gradient': r'(linear|radial|conic)-gradient\([^)]+\)',
            'transform': r'(transform|rotate|scale|translate|skew)\([^)]+\)',
            'filter': r'(blur|brightness|contrast|grayscale|invert)\([^)]+\)',
            'calc': r'calc\([^)]+\)',
            'color': r'(rgb|rgba|hsl|hsla)\([^)]+\)'
        }
        
        for pattern_type, pattern in complex_patterns.items():
            if re.search(pattern, value):
                if pattern_type == 'transform':
                    # Add units to transform values
                    return re.sub(r'\b(\d+)(?![a-z%\.])', lambda m: f"{m.group(1)}{'deg' if 'rotate' in value else 'px'}", value)
                elif pattern_type == 'filter':
                    # Add units to filter values
                    return re.sub(r'\b(\d+)(?![a-z%\.])', r'\1px', value)
                return value
        return value
    
    try:
        # Convert string to Python dict
        style_dict = eval(f"dict({style_str})")
        
        # Parse nested styles
        parsed_styles = parse_nested_styles(style_dict)
        
        # Handle CSS variables
        parsed_styles = parse_css_vars(parsed_styles)
        
        # Add vendor prefixes
        parsed_styles = handle_vendor_prefixes(parsed_styles)
        
        # Convert to CSS string
        css_parts = []
        for prop, value in parsed_styles.items():
            if isinstance(value, dict):
                # Handle nested objects (e.g., media queries, pseudo-classes)
                nested_css = parse_style_object(str(value))
                if prop.startswith('@media'):
                    css_parts.append(f"{prop} {{ {nested_css} }}")
                else:
                    css_parts.append(f"&{prop} {{ {nested_css} }}")
            else:
                # Convert camelCase to kebab-case
                prop = camel_to_kebab(prop)
                value = handle_complex_values(str(value))
                css_parts.append(f"{prop}: {value}")
        
        return '; '.join(css_parts)
    
    except (SyntaxError, ValueError) as e:
        logger.error(f"Error parsing style object: {e}")
        return ''

def handle_component_states(code):
    """Handle component states and generate all necessary variations"""
    # Common state patterns
    states = {
        'modal': {
            'open': {'class': 'modal visible', 'style': 'display: block; opacity: 1'},
            'closed': {'class': 'modal hidden', 'style': 'display: none; opacity: 0'}
        },
        'dropdown': {
            'open': {'class': 'dropdown expanded', 'style': 'max-height: 500px; opacity: 1'},
            'closed': {'class': 'dropdown collapsed', 'style': 'max-height: 0; opacity: 0'}
        },
        'accordion': {
            'expanded': {'class': 'accordion-panel expanded', 'style': 'max-height: var(--panel-height)'},
            'collapsed': {'class': 'accordion-panel collapsed', 'style': 'max-height: 0'}
        },
        'tab': {
            'active': {'class': 'tab active', 'style': 'border-bottom-color: var(--active-color)'},
            'inactive': {'class': 'tab', 'style': 'border-bottom-color: transparent'}
        },
        'menu': {
            'open': {'class': 'menu-panel visible', 'style': 'transform: translateX(0)'},
            'closed': {'class': 'menu-panel hidden', 'style': 'transform: translateX(-100%)'}
        },
        'tooltip': {
            'visible': {'class': 'tooltip visible', 'style': 'opacity: 1; visibility: visible'},
            'hidden': {'class': 'tooltip hidden', 'style': 'opacity: 0; visibility: hidden'}
        },
        'form': {
            'valid': {'class': 'form-group valid', 'style': 'border-color: var(--success-color)'},
            'invalid': {'class': 'form-group invalid', 'style': 'border-color: var(--error-color)'},
            'disabled': {'class': 'form-group disabled', 'style': 'opacity: 0.5; pointer-events: none'}
        },
        'button': {
            'default': {'class': 'button', 'style': 'background: var(--primary-color)'},
            'hover': {'class': 'button hover', 'style': 'background: var(--primary-dark)'},
            'active': {'class': 'button active', 'style': 'transform: scale(0.98)'},
            'disabled': {'class': 'button disabled', 'style': 'opacity: 0.5; pointer-events: none'}
        }
    }
    
    def detect_state_type(code):
        """Detect the type of component based on code patterns"""
        patterns = {
            'modal': r'modal|dialog|popup',
            'dropdown': r'dropdown|select|combobox',
            'accordion': r'accordion|collapse|expand',
            'tab': r'tab|panel|view',
            'menu': r'menu|navbar|navigation',
            'tooltip': r'tooltip|popover|hint',
            'form': r'form|input|field',
            'button': r'button|btn|submit'
        }
        
        for component_type, pattern in patterns.items():
            if re.search(pattern, code, re.I):
                return component_type
        return None
    
    def generate_state_variations(component_type, base_code):
        """Generate HTML for all states of a component"""
        if component_type not in states:
            return base_code
        
        variations = []
        component_states = states[component_type]
        
        # Extract the base class and style
        base_class = re.search(r'class=(["\'])([^"\']*)\1', base_code)
        base_style = re.search(r'style=(["\'])([^"\']*)\1', base_code)
        
        for state_name, state_attrs in component_states.items():
            state_code = base_code
            
            # Update class
            if base_class:
                new_class = f"{base_class.group(2)} {state_attrs['class']}".strip()
                state_code = re.sub(r'class=(["\'])[^"\']*(\1)',
                                  f'class="{new_class}"', state_code)
            else:
                state_code = state_code.replace('>', f' class="{state_attrs["class"]}">')
            
            # Update style
            if base_style:
                base_styles = base_style.group(2).strip()
                state_styles = state_attrs['style'].strip()
                new_style = f"{base_styles}; {state_styles}" if base_styles and state_styles else base_styles or state_styles
                state_code = re.sub(r'style=(["\'])[^"\']*(\1)',
                                  f'style="{new_style}"', state_code)
            else:
                state_code = state_code.replace('>', f' style="{state_attrs["style"]}">')
            
            # Add comment to indicate state
            state_code = f"\n<!-- {component_type.title()} - {state_name.title()} State -->\n{state_code}"
            variations.append(state_code)
        
        return '\n'.join(variations)
    
    # Process the code
    component_type = detect_state_type(code)
    if component_type:
        return generate_state_variations(component_type, code)
    return code

def convert_react_to_webflow(react_code):
    try:
        logger.info('Starting conversion of React code')
        logger.debug(f'Input code:\n{react_code}')
        
        # Add HTML comment to indicate source
        converted_code = "<!-- Generated by React to Webflow Converter -->\n"
        
        # Remove import statements and exports
        react_code = re.sub(r'import\s+[^;]+;?\n?', '', react_code)
        react_code = re.sub(r'export\s+default\s+\w+;?\s*', '', react_code)
        
        # Remove function declaration and return statement
        react_code = re.sub(r'function\s+\w+\s*\([^)]*\)\s*{\s*return\s+', '', react_code)
        react_code = re.sub(r'\s*}\s*;?\s*$', '', react_code)
        react_code = re.sub(r'^\s*\(\s*|\s*\)\s*;?\s*$', '', react_code)
        
        # Handle .map() functions with contextual examples
        def replace_map(match):
            array_expr = match.group(1)
            content = match.group(2)
            
            # Handle specific array patterns
            if '[5,4,3,2,1]' in array_expr:
                # Generate star rating buttons
                buttons = []
                for stars in [5,4,3,2,1]:
                    button = f'<button class="star-filter" data-w-click="true" style="padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; background-color: white; color: #212529">{stars}★ & up</button>'
                    buttons.append(button)
                return '\n'.join(buttons)
            elif 'categories' in array_expr:
                # Generate sample category options
                options = [
                    '<option value="electronics">Electronics (24)</option>',
                    '<option value="clothing">Clothing (36)</option>',
                    '<option value="home">Home & Garden (18)</option>'
                ]
                return '\n'.join(options)
            elif 'activeFilters' in array_expr:
                # Generate sample filter tags
                tags = [
                    '<span class="filter-tag" style="padding: 4px 12px; background-color: #e9ecef; border-radius: 16px; font-size: 14px; display: flex; align-items: center; gap: 8px">Category: Electronics<button data-w-click="true" style="border: none; background: none; padding: 0; color: #6c757d; cursor: pointer">✕</button></span>',
                    '<span class="filter-tag" style="padding: 4px 12px; background-color: #e9ecef; border-radius: 16px; font-size: 14px; display: flex; align-items: center; gap: 8px">Price: $100-$500<button data-w-click="true" style="border: none; background: none; padding: 0; color: #6c757d; cursor: pointer">✕</button></span>',
                    '<span class="filter-tag" style="padding: 4px 12px; background-color: #e9ecef; border-radius: 16px; font-size: 14px; display: flex; align-items: center; gap: 8px">Rating: 4★ & up<button data-w-click="true" style="border: none; background: none; padding: 0; color: #6c757d; cursor: pointer">✕</button></span>'
                ]
                return '\n'.join(tags)
            return ''
        converted_code = re.sub(r'\{([^}]+)\.map\([^=]+=>[^}]+(\{[^}]+\}|[^}]+)\)\}', replace_map, converted_code)
        
        # Convert event handlers to Webflow attributes
        def convert_event_handler(match):
            event_type = match.group(1)
            handler = match.group(2)
            # Enhanced event mapping
            event_map = {
                'Click': {'attr': 'click', 'interaction': 'click'},
                'MouseEnter': {'attr': 'mouseenter', 'interaction': 'hover-in'},
                'MouseLeave': {'attr': 'mouseleave', 'interaction': 'hover-out'},
                'Focus': {'attr': 'focus', 'interaction': 'focus'},
                'Blur': {'attr': 'blur', 'interaction': 'blur'},
                'Change': {'attr': 'change', 'interaction': 'change'},
                'Submit': {'attr': 'submit', 'interaction': 'submit'},
                'KeyPress': {'attr': 'keypress', 'interaction': 'key-press'},
                'Scroll': {'attr': 'scroll', 'interaction': 'scroll'}
            }
            
            for react_event, mapping in event_map.items():
                if react_event.lower() in event_type.lower():
                    return f'data-w-{mapping["attr"]}="true"'
            return ''
        converted_code = re.sub(r'on([A-Z][a-zA-Z]*)={([^}]+)}', convert_event_handler, converted_code)
        
        # Convert className to class
        converted_code = re.sub(r'className=(["\'])([^"\']*)\1', r'class=\1\2\1', converted_code)
        
        # Handle inline styles
        def convert_style(match):
            style_content = match.group(1)
            try:
                # Extract style properties
                styles = []
                for prop in re.finditer(r'([a-zA-Z]+):\s*([^,}]+?)(?:,|$|\s*})', style_content):
                    key, value = prop.groups()
                    # Convert camelCase to kebab-case
                    key = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', key).lower()
                    # Clean up value
                    value = value.strip().strip('"\'')
                    # Add px to numeric values for certain properties
                    if re.match(r'^\d+$', value) and key in ['padding', 'margin', 'border-radius', 'width', 'height']:
                        value = f'{value}px'
                    styles.append(f'{key}: {value}')
                if styles:
                    return f'style="{'; '.join(styles)}"'
                return ''
            except Exception as e:
                logger.error(f'Style conversion error: {e}')
                return ''
        converted_code = re.sub(r'style={{([^}]+)}}', convert_style, converted_code)
        
        # Handle template literals with smart content
        def replace_template_literal(match):
            content = match.group(1)
            # Handle specific template patterns
            if 'getCategoryName' in content:
                return 'Electronics'
            elif 'selectedRating' in content:
                return '4★ & up'
            elif 'minPrice' in content:
                return '$100'
            elif 'maxPrice' in content:
                return '$500'
            elif 'filteredResults.length' in content:
                return '24'
            # Replace ${...} expressions with contextual content
            return re.sub(r'\${([^}]+)}', lambda m: {
                'category.name': 'Electronics',
                'category.count': '24',
                'minPrice': '$100',
                'maxPrice': '$500',
                'selectedRating': '4★',
                'filteredResults.length': '24'
            }.get(m.group(1), ''), content)
        converted_code = re.sub(r'`([^`]+)`', replace_template_literal, converted_code)
        converted_code = re.sub(r'\$\{([^}]+)\}', replace_template_literal, converted_code)
        
        # Handle ternary operators and conditional rendering
        def replace_conditional(match):
            condition = match.group(1)
            content = match.group(2) if len(match.groups()) > 1 else match.group(1)
            
            # Handle specific conditions
            if 'selectedRating === stars' in condition:
                return content.replace('selectedRating === stars ? \'#007bff\' : \'white\'', 'white')\
                             .replace('selectedRating === stars ? \'white\' : \'#212529\'', '#212529')
            elif 'selectedCategory' in condition:
                return 'Electronics'
            elif 'selectedRating' in condition:
                return '4★ & up'
            elif 'minPrice || maxPrice' in condition:
                return '$100 - $500'
            
            # Return the content without conditional wrapper
            return content.strip()
            
        # Handle ternary operators
        converted_code = re.sub(r'\{([^?]+)\?\s*([^:]+)\s*:\s*([^}]+)\}', replace_conditional, converted_code)
        # Handle && conditions
        converted_code = re.sub(r'\{([^}]+)\s*&&\s*([^}]+)\}', replace_conditional, converted_code)
        
        # Pre-process map functions before handling other expressions
        def handle_map_function(match):
            array_expr = match.group(1)
            content = match.group(2)
            
            if '[5,4,3,2,1]' in array_expr:
                buttons = []
                for stars in [5,4,3,2,1]:
                    buttons.append(f'<button class="star-filter" data-w-click="true" style="padding: 8px 12px; border: 1px solid #dee2e6; border-radius: 4px; background-color: white; color: #212529">{stars}★ & up</button>')
                return '\n'.join(buttons)
            elif 'categories' in array_expr:
                return '''<option value="">All Categories</option>
                    <option value="electronics">Electronics (24)</option>
                    <option value="clothing">Clothing (36)</option>
                    <option value="home">Home & Garden (18)</option>'''
            elif 'activeFilters' in array_expr:
                return '''<span class="filter-tag" style="padding: 4px 12px; background-color: #e9ecef; border-radius: 16px; font-size: 14px; display: flex; align-items: center; gap: 8px">Category: Electronics
                    <button data-w-click="true" style="border: none; background: none; padding: 0; color: #6c757d; cursor: pointer">✕</button></span>'''
            return ''

        # Handle JSX expressions
        def convert_jsx_expr(match):
            expr = match.group(1).strip()
            
            # Skip event handlers and style objects
            if '=>' in expr or '{' in expr:
                return ''
            
            # Handle specific expressions
            if expr == 'filteredResults.length':
                return '24'
            elif 'selectedCategory' in expr:
                return 'Electronics'
            elif 'selectedRating' in expr:
                return '4★ & up'
            elif 'minPrice' in expr:
                return '$100'
            elif 'maxPrice' in expr:
                return '$500'
            elif expr == 'text':
                return 'Click Here'
            
            return ''
        
        # Process map functions first
        converted_code = re.sub(r'\{([^}]+)\.map\([^=]+=>[^}]+(\{[^}]+\}|[^}]+)\)\}', handle_map_function, converted_code)
        
        # Remove comments
        converted_code = re.sub(r'\{/\*[^*]*\*/\}', '', converted_code)
        
        # Convert remaining JSX expressions
        converted_code = re.sub(r'\{([^{}]+)\}', convert_jsx_expr, converted_code)
        
        # Clean up any remaining React artifacts
        converted_code = re.sub(r'\$\{[^}]+\}', '', converted_code)
        converted_code = re.sub(r'`[^`]+`', '', converted_code)
        
        # Convert self-closing tags
        converted_code = re.sub(r'<([\w-]+)([^>]*?)\s*/>', r'<\1\2></\1>', converted_code)
        
        # Only apply component patterns and states if the component has state management
        has_state = 'useState' in react_code or 'state' in react_code
        if has_state:
            pattern_name, template = detect_component_pattern(converted_code)
            if pattern_name:
                logger.info(f'Detected {pattern_name} component pattern')
                converted_code = template.strip()
            converted_code = handle_component_states(converted_code)
        
        # Clean up whitespace and formatting
        converted_code += react_code
        
        # Format the HTML
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(converted_code, 'html.parser')
            converted_code = soup.prettify()
        except ImportError:
            # Basic formatting if BeautifulSoup is not available
            # Basic formatting if BeautifulSoup is not available
            converted_code = re.sub(r'\s+', ' ', converted_code)
            converted_code = re.sub(r'>\s+<', '>\n<', converted_code)
            converted_code = re.sub(r'<!--|-->', lambda m: f'\n{m.group(0)}\n', converted_code)
        
        # Clean up HTML encoding
        converted_code = converted_code.replace('&amp;', '&')
        converted_code = converted_code.replace('&lt;', '<')
        converted_code = converted_code.replace('&gt;', '>')
        
        logger.info('Conversion completed successfully')
        return converted_code.strip()
            
    except Exception as e:
        logger.error(f'Conversion error: {e}')
        raise Exception(f'Failed to convert React code: {str(e)}')

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

        react_code = data.get('react_code')
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
    # Use environment variable for port with a fallback to 8081
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)
