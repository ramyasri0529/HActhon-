document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const sourceCode = document.getElementById('sourceCode');
    const loader = document.getElementById('loader');
    const testCodeOut = document.getElementById('testCodeOut');
    const analysisOut = document.getElementById('analysisOut');
    const coverageOut = document.getElementById('coverageOut');
    const copyBtn = document.getElementById('copyBtn');

    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        const activePane = document.querySelector('.tab-pane.active textarea');
        if (activePane && activePane.value) {
            navigator.clipboard.writeText(activePane.value).then(() => {
                const icon = copyBtn.querySelector('i');
                icon.className = 'fa-solid fa-check';
                setTimeout(() => {
                    icon.className = 'fa-regular fa-copy';
                }, 2000);
            });
        }
    });

    // Generate Button Click
    generateBtn.addEventListener('click', async () => {
        const code = sourceCode.value.trim();
        if (!code) {
            alert('Please paste some Python code first!');
            return;
        }

        // Show Loader
        loader.classList.remove('hidden');
        generateBtn.disabled = true;
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code })
            });

            const data = await response.json();

            if (data.error) {
                testCodeOut.value = `Error: ${data.error}\n\n${data.traceback || ''}`;
                analysisOut.value = '';
                coverageOut.value = '';
            } else {
                testCodeOut.value = data.test_code || 'No tests generated.';
                analysisOut.value = data.analysis || 'No analysis available.';
                coverageOut.value = data.coverage || 'Coverage check failed.';
                
                // Switch to tests tab automatically
                tabBtns[0].click();
            }
        } catch (error) {
            console.error('Error:', error);
            testCodeOut.value = `Failed to connect to the server.\n\n${error}`;
        } finally {
            // Hide Loader
            loader.classList.add('hidden');
            generateBtn.disabled = false;
        }
    });
    
    // Add some sample default text if empty
    if(!sourceCode.value.trim()) {
        sourceCode.value = `import math\n\nclass Calculator:\n    def add(self, a, b):\n        return a + b\n\n    def sqrt(self, a):\n        if a < 0:\n            raise ValueError("Negative number")\n        return math.sqrt(a)\n`;
    }
});
