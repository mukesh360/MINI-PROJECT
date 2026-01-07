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

  const question = currentInput;

  // 1️⃣ Add USER message
  setMessages(prev => [
    ...prev,
    {
      id: Date.now(),
      sender: "user",
      text: question
    }
  ]);

  setCurrentInput("");
  setShowChat(true);
  setLoading(true);

  // 2️⃣ Add BOT placeholder
  setMessages(prev => [
    ...prev,
    {
      id: Date.now() + 1,
      sender: "bot",
      text: "",
      citations: []
    }
  ]);

  try {
    // 3️⃣ Call streaming API
    const response = await fetch("http://localhost:8000/query/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    if (!response.body) {
      throw new Error("No response body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let result = "";

    // 4️⃣ Stream tokens
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      result += decoder.decode(value, { stream: true });

      setMessages(prev => [
        ...prev.slice(0, -1),
        {
          ...prev[prev.length - 1],
          text: result
        }
      ]);
    }

  } catch (err) {
    console.error(err);
    setMessages(prev => [
      ...prev.slice(0, -1),
      {
        sender: "bot",
        text: "⚠️ Error talking to backend"
      }
    ]);
  } finally {
    setLoading(false);
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
