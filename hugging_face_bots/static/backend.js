    const startSpeechRecognitionButton = document.getElementById('startSpeechRecognition');
    const stopSpeechRecognitionButton = document.getElementById('stopSpeechRecognition');
    const recognizedTextElement = document.getElementById('recognizedText');
    const processedTextElement = document.getElementById('processedText');
    const synth = window.speechSynthesis;
    let recognition = null;

    startSpeechRecognitionButton.addEventListener('click', () => {
        recognition = new webkitSpeechRecognition() || new SpeechRecognition();
        recognition.continuous = false; // Set continuous to false

        recognition.onstart = () => {
            console.log('Speech recognition started.');
            recognizedTextElement.textContent = 'Recognized Text: Listening...';
        };

        recognition.onresult = (event) => {
            const result = event.results[event.results.length - 1][0].transcript;
            recognizedTextElement.textContent = `Recognized Text: ${result}`;

            // Send the recognized text to the Flask backend
            fetch('/process_user_input', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'user_input': result }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Processed Text:', data.processed_text);
                processedTextElement.textContent = `Processed Text: ${data.processed_text}`;

                // Convert processed text to voice
                const utterance = new SpeechSynthesisUtterance(data.processed_text);
                synth.speak(utterance);
                
                // Stop recognition after processing one input
                recognition.stop(); // Add this line
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
        };

        recognition.start();
    });

    stopSpeechRecognitionButton.addEventListener('click', () => {
        if (recognition) {
            recognition.stop();
            recognizedTextElement.textContent = 'Recognized Text: Stopped.';
        }
    });
