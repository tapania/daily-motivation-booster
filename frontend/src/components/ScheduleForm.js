// frontend/src/components/ScheduleForm.js
import React, { useState } from 'react';

function ScheduleForm({ schedule, setSchedule }) {
  const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const [errors, setErrors] = useState({});

  const handleChange = (day, time) => {
    const newSchedule = schedule.filter(s => s.day_of_week !== day);
    if (time) {
      newSchedule.push({ day_of_week: day, time_of_day: time });
    }
    setSchedule(newSchedule);
    // Clear error for the day if any
    setErrors(prevErrors => ({ ...prevErrors, [day]: '' }));
  };

  const validate = () => {
    const newErrors = {};
    schedule.forEach(s => {
      if (!/^\d{2}:\d{2}$/.test(s.time_of_day)) {
        newErrors[s.day_of_week] = 'Invalid time format.';
      }
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Expose validate function to parent if needed
  // Alternatively, perform validation in the parent component

  return (
    <div className="grid grid-cols-1 gap-4">
      {daysOfWeek.map(day => (
        <div key={day} className="flex items-center">
          <label className="w-32">{day}</label>
          <input
            type="time"
            className={`input input-bordered w-full ${errors[day] ? 'input-error' : ''}`}
            onChange={e => handleChange(day, e.target.value)}
          />
          {errors[day] && <span className="text-red-500 text-sm ml-2">{errors[day]}</span>}
        </div>
      ))}
    </div>
  );
}

export default ScheduleForm;