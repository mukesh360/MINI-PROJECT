// import FileItem from './FileItem';
// import './Sidebar.css';

// function Sidebar({ uploadedFiles, selectedFile, onSelectFile, onDeleteFile }) {
//   return (
//     <div className="sidebar">
//       <div className="sidebar-header">
//         <h2 className="sidebar-title">Purple AI</h2>
//       </div>

//       <div className="sidebar-section">
//         <h3 className="section-title">Conversations</h3>
//         <div className="conversation-item active">
//           <div className="conversation-icon">
//             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//               <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
//             </svg>
//           </div>
//           <span className="conversation-text">Current Chat</span>
//         </div>
//       </div>

//       {uploadedFiles.length > 0 && (
//         <div className="sidebar-section">
//           <h3 className="section-title">Uploaded Files</h3>
//           <div className="files-list">
//             {uploadedFiles.map((file) => (
//               <FileItem
//                 key={file.id}
//                 file={file}
//                 isSelected={selectedFile === file.id}
//                 onSelect={() => onSelectFile(file.id)}
//                 onDelete={() => onDeleteFile(file.id)}
//               />
//             ))}
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default Sidebar;
import { useState } from 'react';
import FileItem from './FileItem';
import './Sidebar.css';

function Sidebar({
  uploadedFiles = [],
  selectedFiles = [],
  onToggleSelect,
  onDeleteFile
}) {
  // ✅ ONLY ONE MENU OPEN AT A TIME
  const [openMenuId, setOpenMenuId] = useState(null);

  // ✅ Wrap select to auto-close menu
  const handleToggleSelect = (fileId) => {
    onToggleSelect(fileId);
    setOpenMenuId(null);
  };

  // ✅ Wrap delete to auto-close menu
  const handleDelete = (fileId) => {
    onDeleteFile(fileId);
    setOpenMenuId(null);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Purple AI</h2>
      </div>

      <div className="sidebar-section">
        <h3 className="section-title">Conversations</h3>
        <div className="conversation-item active">
          <div className="conversation-icon">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <span className="conversation-text">New Chat</span>
        </div>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="sidebar-section">
          <h3 className="section-title">Uploaded Files</h3>

          <div className="files-list">
            {uploadedFiles.map((file) => (
              <FileItem
                key={file.id}
                file={file}
                isSelected={selectedFiles.includes(file.id)}

                /* 🔑 CRITICAL FIX */
                openMenuId={openMenuId}
                setOpenMenuId={setOpenMenuId}

                onToggleSelect={handleToggleSelect}
                onDelete={handleDelete}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Sidebar;
