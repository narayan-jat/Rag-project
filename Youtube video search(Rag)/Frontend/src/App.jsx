import React from 'react';
import FileUpload from './components/FileUpload';
import ChatBot from './components/ChatBot';

const App = () => {
  return (
    <div>
      <h1>RAG Video ChatBot</h1>
      <FileUpload />
      <ChatBot />
    </div>
  );
};

export default App;
