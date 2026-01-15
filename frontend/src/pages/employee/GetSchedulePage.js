
import DecisionFrame from '../../components/DecisionFrame';
import React, { useState, useEffect } from 'react';
import './GetSchedulePage.css';

// Dummy data for demonstration
const dummySchedule = [
  { date: '2026-01-06', shift: '9:00-17:00' },
  { date: '2026-01-10', shift: '13:00-21:00' },
  { date: '2026-01-15', shift: 'OFF' },
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

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const GetSchedulePage = () => {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());
  const days = getMonthDays(year, month);

  // In real app, fetch schedule for the month
  const scheduleMap = Object.fromEntries(dummySchedule.map(s => [s.date, s.shift]));

  return (
    <div className="get-schedule-page">
      <h2>Monthly Schedule</h2>
      <div className="calendar-controls">
        <button onClick={() => setMonth(m => m === 0 ? 11 : m - 1)}>&lt;</button>
        <span>{today.toLocaleString('default', { month: 'long' })} {year}</span>
        <button onClick={() => setMonth(m => m === 11 ? 0 : m + 1)}>&gt;</button>
      </div>
      <div className="calendar-grid">
        {days.map(day => {
          const dateStr = day.toISOString().slice(0, 10);
          return (
            <div key={dateStr} className="calendar-cell">
              <div className="calendar-date">{day.getDate()}</div>
              <div className="calendar-shift">{scheduleMap[dateStr] || '-'}</div>
            </div>
          );
        })}
      </div>
      {/* To mutate schedule, use DecisionFrame modal for all mutations. */}
    </div>
  );
};

export default GetSchedulePage;
