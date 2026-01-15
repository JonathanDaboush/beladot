/**
 * DecisionFrame Component
 *
 * Displays a modal dialog for confirming or cancelling a critical decision.
 * Shows a preview and custom banner if provided.
 *
 * Props:
 *   - visible: Boolean to show/hide the modal
 *   - onCancel: Function to call when cancelling
 *   - onConfirm: Function to call when confirming
 *   - preview: Optional preview text/content
 *   - children: Content to display in the modal body
 *   - banner: Optional custom banner text
 */
import React from 'react';
// ...existing code...

/**
 * Main modal component for decision confirmation.
 */
const DecisionFrame = ({ visible, onCancel, onConfirm, preview, children, banner }) => {
  if (!visible) return null;
  return (
    <div className="modal fade show d-block" tabIndex="-1" style={{ background: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header bg-primary text-white">
            <h5 className="modal-title">{banner || 'You are about to make a permanent operational decision'}</h5>
            <button type="button" className="btn-close" aria-label="Close" onClick={onCancel}></button>
          </div>
          <div className="modal-body">
            {children}
            {preview && <div className="alert alert-info mt-3">{preview}</div>}
          </div>
          <div className="modal-footer">
            <button className="btn btn-success" onClick={onConfirm}>Confirm</button>
            <button className="btn btn-secondary" onClick={onCancel}>Cancel</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DecisionFrame;
