import { useEffect, useRef } from 'react';
import Message from './Message';
import './ChatWindow.css';

function ChatWindow({
  messages,
  currentInput,
  setCurrentInput,
  onSendMessage,
  onFileUpload,
  onKeyPress,
  loading = false, // ✅ NEW
}) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {/* 🧠 MESSAGES */}
      <div className="messages-container">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}

        {/* 🤖 TYPING INDICATOR */}
        {loading && (
          <div className="typing-indicator">
            🤖 AI is thinking...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ⌨️ INPUT */}
      <div className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            className="chat-input"
            placeholder={loading ? "Please wait..." : "Type your message..."}
            value={currentInput}
            onChange={(e) => setCurrentInput(e.target.value)}
            onKeyPress={onKeyPress}
            disabled={loading}
          />

          {/* 📄 FILE UPLOAD */}
          <label className="upload-btn">
            <input
              type="file"
              accept=".pdf,.csv"
              onChange={onFileUpload}
              style={{ display: 'none' }}
              disabled={loading}
            />
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </label>

          {/* 🚀 SEND */}
          <button
            className="send-btn"
            onClick={onSendMessage}
            disabled={loading}
          >
            {loading ? (
              "..."
            ) : (
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
