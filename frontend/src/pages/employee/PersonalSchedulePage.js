import React, { useState } from 'react';
import './PersonalSchedulePage.css';
import DecisionFrame from '../../components/DecisionFrame';

// Dummy PTO/sick data for demonstration
const initialEntries = [
  { date: '2026-01-08', type: 'PTO', note: 'Vacation' },
  { date: '2026-01-12', type: 'Sick', note: 'Flu' },
];

function getMonthDays(year, month) {
  const date = new Date(year, month, 1);
  const days = [];
  while (date.getMonth() === month) {
    days.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return days;
}

const entryTypes = ['PTO', 'Sick'];

const PersonalSchedulePage = () => {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());
  const [entries, setEntries] = useState(initialEntries);
  const [selectedDate, setSelectedDate] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalType, setModalType] = useState('create'); // create | update
  const [form, setForm] = useState({ type: 'PTO', note: '' });
  const [pendingAction, setPendingAction] = useState(null); // 'create' | 'update' | 'delete'
  const [preview, setPreview] = useState('');

  const days = getMonthDays(year, month);
  const entryMap = Object.fromEntries(entries.map(e => [e.date, e]));

  function openCreateModal(dateStr) {
    setSelectedDate(dateStr);
    setForm({ type: 'PTO', note: '' });
    setModalType('create');
    setPendingAction('create');
    setPreview('');
    setModalOpen(true);
  }
  function openEditModal(dateStr) {
    const entry = entryMap[dateStr];
    setSelectedDate(dateStr);
    setForm({ type: entry.type, note: entry.note });
    setModalType('update');
    setPendingAction('update');
    setPreview('');
    setModalOpen(true);
  }
  function handleDeleteRequest() {
    setPendingAction('delete');
    setPreview(`You are about to delete the entry for ${selectedDate}. This action cannot be undone.`);
  }
  function handlePreview() {
    if (pendingAction === 'create') {
      setPreview(`You are about to create a ${form.type} entry for ${selectedDate} with note: "${form.note}".`);
    } else if (pendingAction === 'update') {
      setPreview(`You are about to update the entry for ${selectedDate} to type: ${form.type}, note: "${form.note}".`);
    }
  }
  function handleConfirm() {
    if (pendingAction === 'create') {
      setEntries([...entries, { date: selectedDate, ...form }]);
    } else if (pendingAction === 'update') {
      setEntries(entries.map(e => e.date === selectedDate ? { ...e, ...form } : e));
    } else if (pendingAction === 'delete') {
      setEntries(entries.filter(e => e.date !== selectedDate));
    }
    setModalOpen(false);
    setPreview('');
    setPendingAction(null);
  }
  function handleCancel() {
    setModalOpen(false);
    setPreview('');
    setPendingAction(null);
  }

  return (
    <div className="personal-schedule-page">
      <h2>Personal Schedule (PTO & Sick Days)</h2>
      <div className="calendar-controls">
        <button onClick={() => setMonth(m => m === 0 ? 11 : m - 1)}>&lt;</button>
        <span>{today.toLocaleString('default', { month: 'long' })} {year}</span>
        <button onClick={() => setMonth(m => m === 11 ? 0 : m + 1)}>&gt;</button>
      </div>
      <div className="calendar-grid">
        {days.map(day => {
          const dateStr = day.toISOString().slice(0, 10);
          const entry = entryMap[dateStr];
          return (
            <div
              key={dateStr}
              className={`calendar-cell${entry ? ' has-entry' : ''}`}
              onClick={() => entry ? openEditModal(dateStr) : openCreateModal(dateStr)}
            >
              <div className="calendar-date">{day.getDate()}</div>
              <div className="calendar-entry-type">{entry ? entry.type : ''}</div>
            </div>
          );
        })}
      </div>
      <DecisionFrame
        visible={modalOpen}
        onCancel={handleCancel}
        onConfirm={handleConfirm}
        preview={preview}
        banner={pendingAction === 'delete' ? 'You are about to delete an entry' : undefined}
      >
        <h3>{modalType === 'create' ? 'Add' : 'Edit'} Entry for {selectedDate}</h3>
        {pendingAction !== 'delete' && (
          <>
            <div>
              <label>Type: </label>
              <select value={form.type} onChange={e => setForm({ ...form, type: e.target.value })}>
                {entryTypes.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div>
              <label>Note: </label>
              <input value={form.note} onChange={e => setForm({ ...form, note: e.target.value })} />
            </div>
            <div className="modal-actions">
              <button type="button" onClick={handlePreview}>
                {modalType === 'create' ? 'Preview Create' : 'Preview Update'}
              </button>
              {modalType === 'update' && (
                <button type="button" onClick={handleDeleteRequest}>Delete</button>
              )}
            </div>
          </>
        )}
        {pendingAction === 'delete' && (
          <div className="modal-actions">
            <span>Are you sure you want to delete this entry?</span>
          </div>
        )}
      </DecisionFrame>
    </div>
  );
};

export default PersonalSchedulePage;
