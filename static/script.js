document.addEventListener('DOMContentLoaded', function() {
    console.log('Application initialized');
    // Initialize CodeMirror for React code
    const reactEditor = CodeMirror.fromTextArea(document.getElementById('reactCode'), {
        mode: 'jsx',
        theme: 'monokai',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        lineWrapping: true
    });

    // Initialize CodeMirror for Webflow code
    const webflowEditor = CodeMirror.fromTextArea(document.getElementById('webflowCode'), {
        mode: 'xml',
        theme: 'monokai',
        lineNumbers: true,
        readOnly: true,
        lineWrapping: true
    });

    // Status message function
    function showStatus(message, isError = false) {
        const statusDiv = document.getElementById('statusMessage');
        if (!statusDiv) {
            const div = document.createElement('div');
            div.id = 'statusMessage';
            div.style.padding = '10px';
            div.style.margin = '10px 0';
            div.style.borderRadius = '4px';
            document.querySelector('.container').insertBefore(div, document.querySelector('.grid'));
        }
        const div = document.getElementById('statusMessage');
        div.textContent = message;
        div.style.backgroundColor = isError ? '#fee2e2' : '#dcfce7';
        div.style.color = isError ? '#991b1b' : '#166534';
    }

    // Convert button click handler
    // Add click handler for convert button
    const convertBtn = document.getElementById('convertBtn');
    if (!convertBtn) {
        console.error('Convert button not found!');
        return;
    }

    convertBtn.addEventListener('click', async () => {
        console.log('Convert button clicked');
        const reactCode = reactEditor.getValue();
        
        if (!reactCode.trim()) {
            showStatus('Please enter some React code to convert', true);
            return;
        }

        showStatus('Converting...');
        
        try {
            console.log('Attempting to send code to server:', reactCode);
            showStatus('Sending request to server...');
            
            const url = 'http://localhost:8080/convert';
            console.log('Sending POST request to:', url);
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ code: reactCode })
            });

            console.log('Server response:', response);
            const data = await response.json();
            console.log('Response data:', data);
            
            if (response.ok) {
                webflowEditor.setValue(data.converted_code);
                showStatus('Conversion successful!');
            } else {
                showStatus('Error: ' + (data.error || 'Unknown error occurred'), true);
            }
        } catch (error) {
            console.error('Conversion error:', error);
            showStatus('Error converting code. Check console for details.', true);
        }
    });

    // Copy button click handler
    document.getElementById('copyBtn').addEventListener('click', () => {
        const convertedCode = webflowEditor.getValue();
        if (!convertedCode.trim()) {
            showStatus('No converted code to copy', true);
            return;
        }
        
        navigator.clipboard.writeText(convertedCode)
            .then(() => {
                showStatus('Code copied to clipboard!');
            })
            .catch(err => {
                showStatus('Failed to copy code: ' + err.message, true);
            });
    });

    // Add example button
    const exampleBtn = document.createElement('button');
    exampleBtn.textContent = 'Load Example';
    exampleBtn.className = 'bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-6 rounded-lg transition duration-200';
    document.querySelector('.flex.justify-center.mt-8.space-x-4').appendChild(exampleBtn);

    exampleBtn.addEventListener('click', () => {
        const exampleCode = `function Welcome() {
  return (
    <div className="welcome-container">
      <h1 className="title" style={{color: 'blue', fontSize: '24px'}}>
        Hello, Webflow!
      </h1>
      <button onClick={() => alert('clicked')} className="btn-primary">
        Click me
      </button>
    </div>
  );
}`;
        reactEditor.setValue(exampleCode);
        showStatus('Example code loaded!');
    });
});
