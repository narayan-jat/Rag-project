import re
from groq import Groq

def GroqChat(question):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": question}],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

def generate_answer_with_sources(query, retrieved_chunks):
    
    if not retrieved_chunks:
        return {"response": "It appears that there is no relevant information available on this topic in the database.", "context": "", "sources": []}
    
    unique_contexts = set()
    context_list = []
    
    for chunk in retrieved_chunks:
        video_id = chunk[0].video_id
        start_time = chunk[0].start_time
        text = chunk[0].text
        
        if (video_id, start_time) not in unique_contexts:
            unique_contexts.add((video_id, start_time))
            context_list.append(f"[{video_id} - {start_time}] {text}")
    
    context = " ".join(context_list)
    print(context)
    
    input_text = f"Query: {query}\nContext: {context}\nAnswer:"
    
    response = GroqChat(input_text)
    
    unique_sources = [{"video_id": video_id, "start_time": start_time} for video_id, start_time in unique_contexts]
    
    return {"response": response, "context": context, "sources": unique_sources}
