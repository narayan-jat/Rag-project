import React, { useState } from 'react';
import { uploadCSV } from '../api';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    console.log("File upload triggered");  
    if (!file) {
      alert('Please select a file');
      return;
    }
    
    try {
      const response = await uploadCSV(file);
      setMessage(response.message);
      console.log("Upload successful:", response);  
    } catch (error) {
      setMessage('Failed to upload file.');
    }
  };
  

  return (
    <div>
      <h3>Upload Video Data CSV</h3>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default FileUpload;
