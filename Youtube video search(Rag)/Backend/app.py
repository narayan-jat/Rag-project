from flask import Flask, request, jsonify
import pandas as pd
from services.ingest_service import ingest_video
from config import Config
from database import db
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins=["http://localhost:5173"])

db.init_app(app)

@app.route('/upload', methods=['POST'])
def upload_video_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        data = pd.read_csv(file)

        for _, row in data.iterrows():
            video_data = {
                'video_id': row['video_id'],
                'title': row['title'],
                'description': row['description'],
                'transcript_chunks': parse_transcript_chunks(row['transcript'])
            }
            ingest_video(video_data)

        return jsonify({"message": "File processed and videos ingested successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

def parse_transcript_chunks(transcript_text):
    import ast
    max_chars = 500
    chunks = []
    current_chunk = ""
    current_start_time = None

    try:
        transcript = ast.literal_eval(transcript_text)
    except (ValueError, SyntaxError):
        return []

    for time, text in transcript.items():
        if not current_chunk:
            current_start_time = time

        if len(current_chunk) + len(text) <= max_chars:
            current_chunk += f" {text}"
        else:
            chunks.append({"start_time": current_start_time, "text": current_chunk.strip()})
            current_chunk = text
            current_start_time = time

    if current_chunk:
        chunks.append({"start_time": current_start_time, "text": current_chunk.strip()})
    
    return chunks


from services.retrieval_service import retrieve_top_chunks
from services.generation_service import generate_answer_with_sources

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query')
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        retrieved_chunks = retrieve_top_chunks(user_query)

        response = generate_answer_with_sources(user_query, retrieved_chunks)

        return jsonify(response), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=5000, debug=True)
