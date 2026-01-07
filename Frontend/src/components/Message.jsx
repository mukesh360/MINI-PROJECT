import './Message.css';

function Message({ message }) {
  const isUser = message.sender === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-bubble">
        <p className="message-text">{message.text}</p>

        {/* 🔗 Citations (ONLY for bot messages) */}
        {!isUser && message.citations?.length > 0 && (
          <div className="citations">
            {message.citations.map(c => (
              <a
                key={c.chunk_id}
                href={`http://localhost:8000/pdf/${c.file}#page=${c.page}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                📄 {c.file} — Page {c.page}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Message;
