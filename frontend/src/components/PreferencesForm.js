// frontend/src/components/PreferencesForm.js

import React, { useState, useEffect } from 'react';
import PersonaSelection from './PersonaSelection';
import VoiceSelection from './VoiceSelection';
import ScheduleForm from './ScheduleForm';
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { timezones } from '../utils/timezones';
import { personas } from '../personas';

function PreferencesForm() {
  const [user, setUser] = useState(null);
  const [preferences, setPreferences] = useState({
    first_name: '',
    user_profile: '',
    timezone: '',
    persona: '',
    tone: '',
    voice: '',
  });
  const [schedule, setSchedule] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [scheduleErrors, setScheduleErrors] = useState({});

  useEffect(() => {
    const fetchUserAndSchedule = async () => {
      try {
        const userResponse = await API.get('/me');
        setUser(userResponse.data);
        setPreferences({
          first_name: userResponse.data.first_name || '',
          user_profile: userResponse.data.user_profile || '',
          timezone: userResponse.data.timezone || '',
          persona: userResponse.data.preferences?.persona || '',
          tone: userResponse.data.preferences?.tone || '',
          voice: userResponse.data.preferences?.voice || '',
        });
        // Fetch schedule
        const scheduleResponse = await API.get('/schedule/');
        const scheduleData = scheduleResponse.data.map(s => ({
          day_of_week: s.day_of_week,
          time_of_day: s.time_of_day.substring(0, 5), // Extract 'HH:MM' from 'HH:MM:SS'
        }));
        setSchedule(scheduleData);
      } catch (error) {
        handleError(error);
        setError('Failed to load user information and schedule.');
      }
    };
    fetchUserAndSchedule();
  }, []);
    

  /**
   * Validates the schedule before submission.
   * Ensures that each entry has a valid day and time format.
   * @returns {boolean} - Returns true if the schedule is valid, false otherwise.
   */
  const validateSchedule = () => {
    const validDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const newErrors = {};

    // Check for duplicate days
    const days = schedule.map(s => s.day_of_week);
    const duplicates = days.filter((day, index) => days.indexOf(day) !== index);
    if (duplicates.length > 0) {
      duplicates.forEach(day => {
        newErrors[day] = 'Duplicate day selected.';
      });
    }

    // Validate each schedule entry
    schedule.forEach(s => {
      if (!validDays.includes(s.day_of_week)) {
        newErrors[s.day_of_week] = 'Invalid day selected.';
      }
      if (!s.time_of_day) {
        newErrors[s.day_of_week] = 'Invalid or missing time.';
      }
    });

    setScheduleErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handles form submission.
   * Validates the schedule and submits preferences and schedule data to the backend.
   * @param {Event} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    // Validate Schedule
    if (!validateSchedule()) {
      setError('Please correct the errors in your schedule.');
      return;
    }

    try {
      // Update user info and preferences
      await API.patch('/preferences/', preferences);
      // Update schedule
      await API.post('/schedule/', schedule);
      setMessage('Preferences saved successfully! 🎉');
    } catch (error) {
      handleError(error);
      setError('An error occurred while saving your preferences.');
      setMessage('');
    }
  };

  /**
   * Handles persona selection and updates the corresponding tone.
   * @param {string} personaName - The selected persona name.
   */
    const handlePersonaSelect = (personaName) => {
      const selected = personas.find(p => p.name === personaName);
      if (selected) {
        setPreferences({
          ...preferences,
          persona: selected.name,
          tone: selected.tone,
        });
      }
    };

  if (!user) {
    return <div className="text-center mt-10">Loading user information...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-4">
      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      {/* Success Message */}
      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {message}
        </div>
      )}

      {/* Instructions Pane */}
      <div className="collapse collapse-arrow border border-base-300 bg-base-100 rounded-box">
        <input type="checkbox" />
        <div className="collapse-title text-xl font-medium">
          Need Help Filling Out Your Preferences?
        </div>
        <div className="collapse-content">
          <p className="mt-2">
            Hey there! Let's fine-tune your motivational engine. Fill out the following sections to personalize your experience:
          </p>
          <ul className="list-disc list-inside mt-2">
            <li><strong>First Name:</strong> Let us address you by name for that personal touch.</li>
            <li><strong>User Profile:</strong> Share a bit about yourself to tailor the speeches just for you. You can use <a href="https://copilot.microsoft.com" target="_blank">Copilot</a> to create the profile for you.</li>
            <li><strong>Timezone:</strong> Set your timezone to schedule speeches at the perfect moment.</li>
            <li><strong>Persona & Tone:</strong> Enter the name of your motivational speaker and describe their unique style. Or choose from list of existing ones.</li>
            <li><strong>Voice:</strong> Select a voice that motivates you the most.</li>
            <li><strong>Schedule:</strong> Plan when you want your motivational boosts to arrive.</li>
          </ul>
          <p className="mt-2">Ready to boost your ambitions? Let’s dive in! 🚀</p>
        </div>
      </div>

      {/* User Information Section */}
      <h2 className="text-3xl font-bold mb-4 mt-6">User Information</h2>
      <div className="grid grid-cols-1 gap-4">
        <input
          type="text"
          placeholder="🚀 Your First Name"
          className="input input-bordered w-full"
          value={preferences.first_name}
          onChange={e => setPreferences({ ...preferences, first_name: e.target.value })}
          required
        />
        <textarea
          placeholder="📝 Tell us about yourself..."
          className="textarea textarea-bordered w-full"
          value={preferences.user_profile}
          onChange={e => setPreferences({ ...preferences, user_profile: e.target.value })}
          rows={4}
        ></textarea>
        <select
          className="select select-bordered w-full"
          value={preferences.timezone}
          onChange={e => setPreferences({ ...preferences, timezone: e.target.value })}
          required
        >
          <option value="">⌚ Choose Your Timezone</option>
          {timezones.map(tz => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </div>

      {/* Persona and Tone Section */}
      <h2 className="text-3xl font-bold mt-8 mb-4">Your Motivational Persona</h2>
      <div className="grid grid-cols-1 gap-4">
        <PersonaSelection selectedPersona={preferences.persona} onSelectPersona={handlePersonaSelect} />

        <input
          type="text"
          placeholder="🎤 Persona Name (e.g., Coach Carter)"
          className="input input-bordered w-full"
          value={preferences.persona}
          onChange={e => setPreferences({ ...preferences, persona: e.target.value })}
          required
        />
        <textarea
          placeholder="🗣️ Tone Description (e.g., Energetic and Persuasive)"
          className="textarea textarea-bordered w-full"
          value={preferences.tone}
          onChange={e => setPreferences({ ...preferences, tone: e.target.value })}
          rows={4}
          required
        ></textarea>
      </div>

      {/* Voice Selection Section */}
      <h2 className="text-3xl font-bold mt-8 mb-4">Choose Your Motivational Voice</h2>
      <VoiceSelection
        selectedVoice={preferences.voice}
        setSelectedVoice={(voice) => setPreferences({ ...preferences, voice })}
      />

      {/* Schedule Form Section */}
      <h2 className="text-3xl font-bold mt-8 mb-4">Set Your Motivation Schedule</h2>
      <ScheduleForm schedule={schedule} setSchedule={setSchedule} />
      {/* Display Schedule Errors if Any */}
      {Object.keys(scheduleErrors).length > 0 && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          Please fix the errors in your schedule.
        </div>
      )}

      {/* Submit Button */}
      <button type="submit" className="btn btn-primary mt-8 w-full">
        Save Preferences 🛠️
      </button>
    </form>
  );
}

export default PreferencesForm;