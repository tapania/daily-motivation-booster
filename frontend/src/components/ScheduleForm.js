// src/components/ScheduleForm.js
import React, { useState } from 'react';

function ScheduleForm({ schedule, setSchedule }) {
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const handleChange = (day, time) => {
    const newSchedule = schedule.filter(s => s.day_of_week !== day);
    if (time) {
      newSchedule.push({ day_of_week: day, time_of_day: time });
    }
    setSchedule(newSchedule);
  };

  return (
    <div className="grid grid-cols-1 gap-4">
      {daysOfWeek.map(day => (
        <div key={day} className="flex items-center">
          <label className="w-32">{day}</label>
          <input
            type="time"
            className="input input-bordered w-full"
            onChange={e => handleChange(day, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
}

export default ScheduleForm;
