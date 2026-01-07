import './Message.css';

function Message({ message }) {
  const isUser = message.sender === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-bubble">
        <p className="message-text">{message.text}</p>
      </div>
    </div>
  );
}

export default Message;
