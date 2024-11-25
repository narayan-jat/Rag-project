from models import Video, VideoChunk
from database import db
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def retrieve_top_chunks(query, top_k=5, similarity_threshold=0.3):
    query_embedding = sbert_model.encode(query).reshape(1, -1)

    all_videos = db.session.query(Video).all()
    video_scores = [(video, cosine_similarity(query_embedding, [video.sbert_embedding])[0][0]) for video in all_videos]
    
    filtered_videos = [(video, score) for video, score in video_scores if score >= similarity_threshold]
    top_videos = sorted(filtered_videos, key=lambda x: x[1], reverse=True)[:top_k]

    results = []
    for video, score in top_videos:
        chunks = db.session.query(VideoChunk).filter_by(video_id=video.video_id).all()
        chunk_scores = [(chunk, cosine_similarity(query_embedding, [chunk.sbert_embedding])[0][0]) for chunk in chunks]
        top_chunks = sorted(chunk_scores, key=lambda x: x[1], reverse=True)[:3]
        
        filtered_chunks = [(chunk, score) for chunk, score in top_chunks if score >= similarity_threshold]
        results.extend(filtered_chunks)

    return results
