import React, { useState } from 'react';
import { getChatResponse } from '../api';
import './ChatBot.css'; 

const ChatBot = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return;

    try {
      const chatResponse = await getChatResponse(query);
      console.log("Chat response:", chatResponse);
      setResponse(chatResponse);
    } catch (error) {
      setResponse({ error: 'Failed to fetch response.' });
    }
  };

  return (
    <div className="chatbot-container">
      <h3>Ask the ChatBot</h3>
      <form onSubmit={handleSubmit} className="chatbot-form">
        <input
          type="text"
          placeholder="Enter your query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="chatbot-input"
        />
        <button type="submit" className="chatbot-button">Ask</button>
      </form>
      {response && (
        <div className="response-container">
          {response.error ? (
            <p className="error-message">{response.error}</p>
          ) : (
            <div className="response-comparison">
              <div className="retrieval-context">
                <h4>Retrieved Context</h4>
                <p>{response.context}</p>
                {/* <div className="sources">
                  {response.sources.map((source, idx) => (
                    <a
                      key={idx}
                      href={`https://www.youtube.com/watch?v=${source.video_id}&t=${source.start_time}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="video-link"
                    >
                      Video Link {idx + 1}
                    </a>
                  ))}
                </div> */}
              </div>

              <div className="generated-response">
                <h4>Generated Response</h4>
                <p>{response.response}</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatBot;
