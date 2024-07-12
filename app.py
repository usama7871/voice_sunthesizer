from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import soundfile as sf
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
import logging

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load models
try:
    encoder.load_model('Real-Time-Voice-Cloning/saved_models/encoder.pt')
    synthesizer = Synthesizer('Real-Time-Voice-Cloning/saved_models/synthesizer.pt')
    vocoder.load_model('Real-Time-Voice-Cloning/saved_models/vocoder.pt')
except Exception as e:
    logging.error(f'Failed to load models: {str(e)}')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'voiceSample' not in request.files or 'textInput' not in request.form:
        return jsonify({'error': 'No file or text provided'}), 400

    voice_sample = request.files['voiceSample']
    text_input = request.form['textInput']

    if voice_sample.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(voice_sample.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    voice_sample.save(file_path)

    try:
        processed_audio_path = voice_cloning(file_path, text_input)
        return send_file(processed_audio_path, mimetype='audio/wav')
    except Exception as e:
        logging.error(f'Error processing audio: {str(e)}')
        return jsonify({'error': 'Failed to process audio'}), 500

def voice_cloning(file_path, text_input):
    original_wav, sampling_rate = sf.read(file_path)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)

    specs = synthesizer.synthesize_spectrograms([text_input], [embed])
    spec = specs[0]

    generated_wav = vocoder.infer_waveform(spec)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated.wav')
    sf.write(output_path, generated_wav, synthesizer.sample_rate)

    return output_path

if __name__ == '__main__':
    app.run(debug=True)
