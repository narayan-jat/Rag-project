from models import Video, VideoChunk
from database import db
from sentence_transformers import SentenceTransformer

sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def ingest_video(video_data):
    video = Video(
        video_id=video_data['video_id'], 
        title=video_data['title'],
        description=video_data['description'],
        sbert_embedding=sbert_model.encode(f"{video_data['title']} {video_data['description']}").tolist(),
        transcript_chunks=video_data['transcript_chunks']
    )
    db.session.add(video)
    db.session.commit()

    for chunk in video_data['transcript_chunks']:
        chunk_embedding = sbert_model.encode(chunk['text']).tolist()
        video_chunk = VideoChunk(
            video_id=video_data['video_id'], 
            start_time=chunk['start_time'],
            text=chunk['text'],
            sbert_embedding=chunk_embedding
        )
        db.session.add(video_chunk)
    db.session.commit()
