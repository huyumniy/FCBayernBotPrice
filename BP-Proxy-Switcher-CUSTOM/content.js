

function createInputField(data) {
    
    const input = document.createElement('input');
    input.type = 'text';
    input.value = data;
    input.id = 'proxyInput';
    input.style.position = 'fixed';
    input.style.top = '10px';
    input.style.right = '10px';
    input.style.zIndex = '1000';

    document.body.appendChild(input);
}


function updateInputField(data) {
    const input = document.getElementById('proxyInput');
    if (input) {
        input.value = data;
    }
}

// Retrieve data from Chrome storage
chrome.storage.local.get(['data'], (result) => {
    if (result.data) {
        console.log('Data retrieved in content.js:', result.data);

        const existingInput = document.getElementById('proxyInput');
        if (existingInput) updateInputField(result.data);
        else createInputField(result.data);
    }
});
