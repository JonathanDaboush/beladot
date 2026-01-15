import React, { useState } from 'react';
import './BookShiftPage.css';
import DecisionFrame from '../../components/DecisionFrame';

// Dummy available shifts for demonstration
const availableShifts = [
  { id: 1, date: '2026-01-09', time: '9:00-17:00' },
  { id: 2, date: '2026-01-13', time: '13:00-21:00' },
  { id: 3, date: '2026-01-18', time: '8:00-16:00' },
];

const BookShiftPage = () => {
  const [booked, setBooked] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedShift, setSelectedShift] = useState(null);
  const [preview, setPreview] = useState('');

  function openBookModal(shift) {
    setSelectedShift(shift);
    setPreview('');
    setModalOpen(true);
  }

  function handlePreview() {
    if (selectedShift) {
      setPreview(`You are about to book the shift on ${selectedShift.date} (${selectedShift.time}). This action is permanent.`);
    }
  }

  function handleConfirm() {
    if (selectedShift) {
      setBooked([...booked, selectedShift.id]);
    }
    setModalOpen(false);
    setPreview('');
    setSelectedShift(null);
  }

  function handleCancel() {
    setModalOpen(false);
    setPreview('');
    setSelectedShift(null);
  }

  return (
    <div className="book-shift-page">
      <h2>Book a Shift</h2>
      <div className="shift-list">
        {availableShifts.map(shift => (
          <div key={shift.id} className="shift-row">
            <div className="shift-date">{shift.date}</div>
            <div className="shift-time">{shift.time}</div>
            <button
              disabled={booked.includes(shift.id)}
              onClick={() => openBookModal(shift)}
            >
              {booked.includes(shift.id) ? 'Booked' : 'Book'}
            </button>
          </div>
        ))}
      </div>
      <DecisionFrame
        visible={modalOpen}
        onCancel={handleCancel}
        onConfirm={handleConfirm}
        preview={preview}
      >
        <h3>Book Shift</h3>
        {selectedShift && (
          <>
            <div>Date: {selectedShift.date}</div>
            <div>Time: {selectedShift.time}</div>
            <div className="modal-actions">
              <button type="button" onClick={handlePreview}>Preview Booking</button>
            </div>
          </>
        )}
      </DecisionFrame>
    </div>
  );
};

export default BookShiftPage;
