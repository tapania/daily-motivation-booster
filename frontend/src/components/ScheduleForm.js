// frontend/src/components/ScheduleForm.js

import React, { useState } from 'react';

function ScheduleForm({ schedule, setSchedule }) {
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const [errors, setErrors] = useState({});

  const hours = [...Array(24).keys()].map(h => h.toString().padStart(2, '0') + ':00');

  const getTimeForDay = (day) => {
    const scheduleEntry = schedule.find(s => s.day_of_week === day);
    return scheduleEntry ? scheduleEntry.time_of_day : '';
  };

  const handleChange = (day, time) => {
    const newSchedule = schedule.filter(s => s.day_of_week !== day);
    if (time) {
      newSchedule.push({ day_of_week: day, time_of_day: time });
    }
    setSchedule(newSchedule);
    // Clear error for the day if any
    setErrors(prevErrors => ({ ...prevErrors, [day]: '' }));
  };

  return (
    <div className="grid grid-cols-1 gap-4">
      {daysOfWeek.map(day => (
        <div key={day} className="flex items-center">
          <label className="w-32">{day}</label>
          <select
            className={`select select-bordered w-full ${errors[day] ? 'input-error' : ''}`}
            value={getTimeForDay(day)}
            onChange={e => handleChange(day, e.target.value)}
          >
            <option value="">Select Time</option>
            {hours.map(time => (
              <option key={time} value={time}>{time}</option>
            ))}
          </select>
          {errors[day] && <span className="text-red-500 text-sm ml-2">{errors[day]}</span>}
        </div>
      ))}
    </div>
  );
}

export default ScheduleForm;