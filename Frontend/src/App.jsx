// import { useState } from 'react';
// import Sidebar from './components/Sidebar';
// import ChatWindow from './components/ChatWindow';
// import './App.css';

// function App() {
//   const [messages, setMessages] = useState([]);
//   const [uploadedFiles, setUploadedFiles] = useState([]);
//   const [selectedFile, setSelectedFile] = useState(null);
//   const [currentInput, setCurrentInput] = useState('');
//   const [showChat, setShowChat] = useState(false);

//   const handleSendMessage = () => {
//     if (currentInput.trim() === '') return;

//     const newMessage = {
//       id: Date.now(),
//       text: currentInput,
//       sender: 'user',
//     };

//     setMessages([...messages, newMessage]);
//     setCurrentInput('');
//     setShowChat(true);

//     setTimeout(() => {
//       const botResponse = {
//         id: Date.now() + 1,
//         text: 'This is a demo response from the AI assistant. Your message has been received and processed.',
//         sender: 'bot',
//       };
//       setMessages((prev) => [...prev, botResponse]);
//     }, 1000);
//   };

//   const handleFileUpload = (event) => {
//     const file = event.target.files[0];
//     if (!file) return;

//     const newFile = {
//       id: Date.now(),
//       name: file.name,
//       type: file.type,
//       size: file.size,
//     };

//     setUploadedFiles([...uploadedFiles, newFile]);
//     setShowChat(true);
//   };

//   const handleDeleteFile = (fileId) => {
//     setUploadedFiles(uploadedFiles.filter((file) => file.id !== fileId));
//     if (selectedFile === fileId) {
//       setSelectedFile(null);
//     }
//   };

//   const handleSelectFile = (fileId) => {
//     setSelectedFile(fileId);
//   };

//   const handleKeyPress = (e) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       handleSendMessage();
//     }
//   };

//   return (
//     <div className="app">
//       {!showChat ? (
//         <div className="home-screen">
//           <div className="home-content">
//             <h1 className="home-title">Ask anything. Get intelligent answers.</h1>
//             <div className="home-input-container">
//               <input
//                 type="text"
//                 className="home-input"
//                 placeholder="Type your message..."
//                 value={currentInput}
//                 onChange={(e) => setCurrentInput(e.target.value)}
//                 onKeyPress={handleKeyPress}
//               />
//               <label className="upload-button">
//                 <input
//                   type="file"
//                   onChange={handleFileUpload}
//                   style={{ display: 'none' }}
//                 />
//                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                   <line x1="12" y1="5" x2="12" y2="19"></line>
//                   <line x1="5" y1="12" x2="19" y2="12"></line>
//                 </svg>
//               </label>
//               <button className="send-button" onClick={handleSendMessage}>
//                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                   <line x1="22" y1="2" x2="11" y2="13"></line>
//                   <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
//                 </svg>
//               </button>
//             </div>
//           </div>
//         </div>
//       ) : (
//         <div className="chat-screen">
//           <Sidebar
//             uploadedFiles={uploadedFiles}
//             selectedFile={selectedFile}
//             onSelectFile={handleSelectFile}
//             onDeleteFile={handleDeleteFile}
//           />
//           <ChatWindow
//             messages={messages}
//             currentInput={currentInput}
//             setCurrentInput={setCurrentInput}
//             onSendMessage={handleSendMessage}
//             onFileUpload={handleFileUpload}
//             onKeyPress={handleKeyPress}
//           />
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;


import { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]); // ✅ ARRAY
  const [currentInput, setCurrentInput] = useState('');
  const [showChat, setShowChat] = useState(false);

  const handleSendMessage = () => {
    if (currentInput.trim() === '') return;

    const newMessage = {
      id: Date.now(),
      text: currentInput,
      sender: 'user',
    };

    setMessages([...messages, newMessage]);
    setCurrentInput('');
    setShowChat(true);

    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        text: 'This is a demo response from the AI assistant. Your message has been received and processed.',
        sender: 'bot',
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const newFile = {
      id: Date.now(),
      name: file.name,
      type: file.type,
      size: file.size,
    };

    setUploadedFiles(prev => [...prev, newFile]);
    setShowChat(true);
  };

  // ✅ MULTI-SELECT TOGGLE
  const handleToggleSelectFile = (fileId) => {
    setSelectedFiles(prev =>
      prev.includes(fileId)
        ? prev.filter(id => id !== fileId)
        : [...prev, fileId]
    );
  };

  // ✅ DELETE + CLEAN SELECTION
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
                  onChange={handleFileUpload}
                  style={{ display: 'none' }}
                />
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19" />
                  <line x1="5" y1="12" x2="19" y2="12" />
                </svg>
              </label>

              <button className="send-button" onClick={handleSendMessage}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="chat-screen">
          <Sidebar
            uploadedFiles={uploadedFiles}
            selectedFiles={selectedFiles}              // ✅ PASS ARRAY
            onToggleSelect={handleToggleSelectFile}    // ✅ PASS TOGGLE
            onDeleteFile={handleDeleteFile}
          />

          <ChatWindow
            messages={messages}
            currentInput={currentInput}
            setCurrentInput={setCurrentInput}
            onSendMessage={handleSendMessage}
            onFileUpload={handleFileUpload}
            onKeyPress={handleKeyPress}
          />
        </div>
      )}
    </div>
  );
}

export default App;
