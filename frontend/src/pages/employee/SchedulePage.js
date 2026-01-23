
import React, { useEffect, useState } from 'react';
import PageHeader from '../../components/PageHeader';
import DepartmentContext from '../../components/DepartmentContext';

// Helper to fetch department calendar from backend
async function fetchDepartmentCalendar(year, month, viewMode = 'self') {
  const res = await fetch(`/api/department_calendar?year=${year}&month=${month}&view_mode=${viewMode}`);
  if (!res.ok) throw new Error('Failed to fetch calendar');
  return res.json();
}

const SchedulePage = ({ currentUser }) => {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [calendar, setCalendar] = useState({});
  const [selectedDay, setSelectedDay] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('self');

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchDepartmentCalendar(year, month, viewMode)
      .then(data => {
        setCalendar(data);
        setLoading(false);
      })
      .catch(e => {
        setError(e.message);
        setLoading(false);
      });
  }, [year, month, viewMode]);

  // Build calendar grid
  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDay = new Date(year, month - 1, 1).getDay();
  const weeks = [];
  let day = 1 - firstDay;
  while (day <= daysInMonth) {
    const week = [];
    for (let i = 0; i < 7; i++) {
      if (day > 0 && day <= daysInMonth) {
        week.push(day);
      } else {
        week.push(null);
      }
      day++;
    }
    weeks.push(week);
  }

  // Find all shifts/pto/sick for a given day
  function getDayEntries(dayNum) {
    const entries = [];
    Object.values(calendar).forEach(emp => {
      emp.shifts.forEach(s => {
        const d = new Date(s.start_time || s.date);
        if (d.getDate() === dayNum) entries.push({ ...s, employee_name: emp.employee_name, type: 'shift' });
      });
      emp.pto.forEach(p => {
        const d = new Date(p.start_date);
        if (d.getDate() === dayNum) entries.push({ ...p, employee_name: emp.employee_name, type: 'pto' });
      });
      emp.sickdays.forEach(s => {
        const d = new Date(s.date);
        if (d.getDate() === dayNum) entries.push({ ...s, employee_name: emp.employee_name, type: 'sick' });
      });
    });
    return entries;
  }

  // Calendar grid cell click
  const handleDayClick = (dayNum) => {
    setSelectedDay(dayNum);
  };

  // Right panel content
  const renderContextPanel = () => {
    if (!selectedDay) return <div className="context-panel-empty">Select a day</div>;
    const entries = getDayEntries(selectedDay);
    return (
      <div className="context-panel">
        <h3>{year}-{String(month).padStart(2, '0')}-{String(selectedDay).padStart(2, '0')}</h3>
        {entries.length === 0 && <div>No shifts, PTO, or sick days.</div>}
        {entries.map((entry, i) => (
          <div key={i} className="context-entry">
            <div><strong>{entry.type === 'shift' ? 'Shift' : entry.type === 'pto' ? 'PTO' : 'Sick Day'}</strong></div>
            <div>Employee: {entry.employee_name}</div>
            {entry.type === 'shift' && (
              <>
                <div>Time: {entry.start_time} - {entry.end_time}</div>
                <div>Status: {entry.status || 'Not started'}</div>
                {/* Clock-in/out buttons shown only if allowed, based on currentUser and entry */}
              </>
            )}
            {entry.type !== 'shift' && (
              <div>Description: {entry.reason || entry.description}</div>
            )}
            {/* Actions (edit/remove) only if allowed by role/ownership, as per backend context */}
          </div>
        ))}
        {/* Action area: create PTO/sick, add/edit shift, etc. based on role/context */}
      </div>
    );
  };

  return (
    <div className="department-calendar-layout">
      <PageHeader
        title="Department Schedule"
        subtitle="View shifts, PTO, and sick days"
      />
      <DepartmentContext />
      <div className="calendar-left-panel">
        <div className="calendar-controls">
          <button onClick={() => setMonth(m => m === 1 ? 12 : m - 1)}>&lt;</button>
          <span>{year} - {String(month).padStart(2, '0')}</span>
          <button onClick={() => setMonth(m => m === 12 ? 1 : m + 1)}>&gt;</button>
          <select value={viewMode} onChange={e => setViewMode(e.target.value)}>
            <option value="self">View as Employee</option>
            <option value="department">View as Department</option>
          </select>
        </div>
        <table className="calendar-grid">
          <thead>
            <tr>{['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(d => <th key={d}>{d}</th>)}</tr>
          </thead>
          <tbody>
            {weeks.map((week, i) => (
              <tr key={i}>
                {week.map((dayNum, j) => (
                  <td key={j} className={dayNum ? 'calendar-day' : 'calendar-empty'} onClick={() => dayNum && handleDayClick(dayNum)}>
                    {dayNum && <div className="calendar-day-num">{dayNum}</div>}
                    {/* Show shift indicator for any, PTO/sick for self only */}
                    {dayNum && getDayEntries(dayNum).some(e => e.type === 'shift') && <div className="shift-dot" />}
                    {dayNum && getDayEntries(dayNum).some(e => e.type === 'pto' && e.employee_name === currentUser.name) && <div className="pto-dot" />}
                    {dayNum && getDayEntries(dayNum).some(e => e.type === 'sick' && e.employee_name === currentUser.name) && <div className="sick-dot" />}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="calendar-right-panel">
        {loading ? <div>Loading...</div> : error ? <div>{error}</div> : renderContextPanel()}
      </div>
    </div>
  );
};

export default SchedulePage;
