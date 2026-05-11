import React from 'react';

function ConfirmDialog({ title, message, confirmText, cancelText, onConfirm, onCancel }) {
  return (
    <div className="confirm-dialog-overlay">
      <div className="confirm-dialog">
        <div className="confirm-dialog-header">
          <span className="confirm-dialog-title">{title}</span>
        </div>
        <div className="confirm-dialog-body">
          <p>{message}</p>
        </div>
        <div className="confirm-dialog-footer">
          <button className="confirm-dialog-btn cancel-btn" onClick={onCancel}>
            {cancelText}
          </button>
          <button className="confirm-dialog-btn confirm-btn" onClick={onConfirm}>
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;
