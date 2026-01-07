// import { useState } from 'react';
// import './FileItem.css';

// function FileItem({ file, isSelected, onSelect, onDelete }) {
//   const [showMenu, setShowMenu] = useState(false);

//   const getFileIcon = () => {
//     if (file.type.includes('image')) {
//       return (
//         <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//           <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
//           <circle cx="8.5" cy="8.5" r="1.5"></circle>
//           <polyline points="21 15 16 10 5 21"></polyline>
//         </svg>
//       );
//     }
//     if (file.type.includes('pdf')) {
//       return (
//         <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//           <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
//           <polyline points="14 2 14 8 20 8"></polyline>
//         </svg>
//       );
//     }
//     return (
//       <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//         <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
//         <polyline points="13 2 13 9 20 9"></polyline>
//       </svg>
//     );
//   };

//   const handleMenuClick = (e) => {
//     e.stopPropagation();
//     setShowMenu(!showMenu);
//   };

//   const handleSelect = () => {
//     onSelect();
//     setShowMenu(false);
//   };

//   const handleDelete = () => {
//     onDelete();
//     setShowMenu(false);
//   };

//   return (
//     <div className={`file-item ${isSelected ? 'selected' : ''}`}>
//       <div className="file-info">
//         <div className="file-icon">{getFileIcon()}</div>
//         <span className="file-name">{file.name}</span>
//       </div>
//       <div className="file-actions">
//         <button className="menu-button" onClick={handleMenuClick}>
//           <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//             <circle cx="12" cy="12" r="1"></circle>
//             <circle cx="12" cy="5" r="1"></circle>
//             <circle cx="12" cy="19" r="1"></circle>
//           </svg>
//         </button>
//         {showMenu && (
//           <div className="dropdown-menu">
//             <button className="menu-item" onClick={handleSelect}>
//               <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                 <polyline points="9 11 12 14 22 4"></polyline>
//                 <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
//               </svg>
//               Select
//             </button>
//             <button className="menu-item delete" onClick={handleDelete}>
//               <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                 <polyline points="3 6 5 6 21 6"></polyline>
//                 <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
//               </svg>
//               Delete
//             </button>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default FileItem;


// import { useState } from 'react';
// import './FileItem.css';

// function FileItem({ file, isSelected, onToggleSelect, onDelete }) {
//   const [showMenu, setShowMenu] = useState(false);

//   const getFileIcon = () => {
//     if (file.type.includes('image')) {
//       return (
//         <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//           <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
//           <circle cx="8.5" cy="8.5" r="1.5" />
//           <polyline points="21 15 16 10 5 21" />
//         </svg>
//       );
//     }

//     if (file.type.includes('pdf')) {
//       return (
//         <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//           <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
//           <polyline points="14 2 14 8 20 8" />
//         </svg>
//       );
//     }

//     return (
//       <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//         <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
//         <polyline points="13 2 13 9 20 9" />
//       </svg>
//     );
//   };

//   const handleMenuClick = (e) => {
//     e.stopPropagation();
//     setShowMenu(prev => !prev);
//   };

//   const handleToggleSelect = (e) => {
//     e.stopPropagation();
//     onToggleSelect(file.id);
//     setShowMenu(false);
//   };

//   const handleDelete = (e) => {
//     e.stopPropagation();
//     onDelete(file.id);
//     setShowMenu(false);
//   };

//   return (
//     <div
//       className={`file-item ${isSelected ? 'selected' : ''}`}
//       onClick={() => onToggleSelect(file.id)}
//     >
//       <div className="file-info">
//         <div className="file-icon">{getFileIcon()}</div>
//         <span className="file-name">{file.name}</span>
//       </div>

//       <div className="file-actions">
//         <button className="menu-button" onClick={handleMenuClick}>
//           <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//             <circle cx="12" cy="12" r="1" />
//             <circle cx="12" cy="5" r="1" />
//             <circle cx="12" cy="19" r="1" />
//           </svg>
//         </button>

//         {showMenu && (
//           <div className="dropdown-menu">
//             <button className="menu-item" onClick={handleToggleSelect}>
//               {isSelected ? 'Unselect' : 'Select'}
//             </button>

//             <button className="menu-item delete" onClick={handleDelete}>
//               Delete
//             </button>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }

// export default FileItem;

import './FileItem.css';

function FileItem({
  file = {},
  isSelected = false,
  openMenuId,              // ✅ from Sidebar
  setOpenMenuId,           // ✅ from Sidebar
  onToggleSelect = () => {},
  onDelete = () => {},
}) {
  const fileType = file?.type ?? '';
  const fileName = file?.name ?? 'Unnamed file';
  const fileId = file?.id ?? null;

  const isMenuOpen = openMenuId === fileId;

  const getFileIcon = () => {
    if (fileType.includes('image')) {
      return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
      );
    }

    if (fileType.includes('pdf')) {
      return (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
        </svg>
      );
    }

    return (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
        <polyline points="13 2 13 9 20 9" />
      </svg>
    );
  };

  const handleMenuClick = (e) => {
    e.stopPropagation();
    setOpenMenuId(isMenuOpen ? null : fileId);
  };

  const handleSelect = (e) => {
    e.stopPropagation();
    onToggleSelect(fileId);
    setOpenMenuId(null);
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    onDelete(fileId);
    setOpenMenuId(null);
  };

  return (
    <div
      className={`file-item ${isSelected ? 'selected' : ''}`}
      onClick={() => onToggleSelect(fileId)}
    >
      <div className="file-info">
        <div className="file-icon">{getFileIcon()}</div>
        <span className="file-name">{fileName}</span>
      </div>

      <div className="file-actions">
        <button className="menu-button" onClick={handleMenuClick}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="1" />
            <circle cx="12" cy="5" r="1" />
            <circle cx="12" cy="19" r="1" />
          </svg>
        </button>

        {isMenuOpen && (
          <div className="dropdown-menu">
            <button className="menu-item" onClick={handleSelect}>
              {isSelected ? 'Unselect' : 'Select'}
            </button>

            <button className="menu-item delete" onClick={handleDelete}>
              Delete
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileItem;
