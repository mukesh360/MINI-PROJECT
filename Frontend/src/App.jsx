import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { uploadFileToBackend, askQuestion } from './api';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [currentInput, setCurrentInput] = useState('');
  const [showChat, setShowChat] = useState(false);
  const [loading, setLoading] = useState(false);

  // 🔹 SEND MESSAGE → BACKEND
const handleSendMessage = async () => {
  if (!currentInput.trim()) return;

  const userMessage = {
    id: Date.now(),
    text: currentInput,
    sender: "user",
  };

  setMessages(prev => [...prev, userMessage]);
  setCurrentInput("");

  try {
    const res = await askQuestion(currentInput, selectedFiles);

    setMessages(prev => [
      ...prev,
      {
        id: Date.now() + 1,
        text: res.answer,
        sender: "bot",
      },
    ]);
  } catch (err) {
    setMessages(prev => [
      ...prev,
      {
        id: Date.now() + 2,
        text: "⚠️ Server error",
        sender: "bot",
      },
    ]);
  }
};


  // 🔹 FILE UPLOAD → BACKEND
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      await uploadFileToBackend(file);

      const newFile = {
        id: Date.now(),
        name: file.name,
        type: file.type,
        size: file.size,
      };

      setUploadedFiles(prev => [...prev, newFile]);
      setShowChat(true);
    } catch (err) {
      alert("File upload failed");
    }
  };

  // 🔹 MULTI-SELECT
  const handleToggleSelectFile = (fileId) => {
    setSelectedFiles(prev =>
      prev.includes(fileId)
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
    );
  };

  const handleDeleteFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
    setSelectedFiles(prev => prev.filter(id => id !== fileId));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="app">
      {!showChat ? (
        <div className="home-screen">
          <div className="home-content">
            <h1 className="home-title">Ask anything. Get intelligent answers.</h1>

            <div className="home-input-container">
              <input
                type="text"
                className="home-input"
                placeholder="Type your message..."
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                onKeyPress={handleKeyPress}
              />

              <label className="upload-button">
                <input
                  type="file"
                  accept=".pdf,.csv"
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />
                +
              </label>

              <button className="send-button" onClick={handleSendMessage}>
                {loading ? "..." : "➤"}
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="chat-screen">
          <Sidebar
            uploadedFiles={uploadedFiles}
            selectedFiles={selectedFiles}
            onToggleSelect={handleToggleSelectFile}
            onDeleteFile={handleDeleteFile}
          />

          <ChatWindow
            messages={messages}
            currentInput={currentInput}
            setCurrentInput={setCurrentInput}
            onSendMessage={handleSendMessage}
            onFileUpload={handleFileUpload}
            onKeyPress={handleKeyPress}
            loading={loading}
          />
        </div>
      )}
    </div>
  );
}

export default App;
