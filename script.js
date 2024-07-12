document.getElementById('voiceForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const voiceSample = document.getElementById('voiceSample').files[0];
    const textInput = document.getElementById('textInput').value;

    if (!voiceSample || !textInput) {
        alert('Please upload a voice sample and enter text.');
        return;
    }

    const formData = new FormData();
    formData.append('voiceSample', voiceSample);
    formData.append('textInput', textInput);

    fetch('YOUR_BACKEND_ENDPOINT', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        const audioUrl = URL.createObjectURL(blob);
        const audioOutput = document.getElementById('audioOutput');
        audioOutput.src = audioUrl;
        audioOutput.load();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating the voice.');
    });
});
fetch('http://localhost:5000/upload', {
    method: 'POST',
    body: formData,
})
.then(response => response.blob())
.then(blob => {
    const audioUrl = URL.createObjectURL(blob);
    const audioOutput = document.getElementById('audioOutput');
    audioOutput.src = audioUrl;
    audioOutput.load();
})
.catch(error => {
    console.error('Error:', error);
    alert('An error occurred while generating the voice.');
});
