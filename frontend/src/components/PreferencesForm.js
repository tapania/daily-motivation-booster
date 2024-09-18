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

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await API.get('/me');
        setUser(response.data);
        setPreferences({
          first_name: response.data.first_name || '',
          user_profile: response.data.user_profile || '',
          timezone: response.data.timezone || '',
          persona: response.data.preferences?.persona || '',
          tone: response.data.preferences?.tone || '',
          voice: response.data.preferences?.voice || '',
        });
      } catch (error) {
        handleError(error);
        setError('Failed to load user information.');
      }
    };

    fetchUser();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      // Update user info and preferences
      await API.post('/preferences/', preferences);
      // Update schedule
      await API.post('/schedule/', schedule);
      setMessage('Preferences saved successfully!');
    } catch (error) {
      handleError(error);
      setError('An error occurred while saving your preferences.');
      setMessage('');
    }
  };

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
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {message}
        </div>
      )}
      <h2 className="text-2xl font-bold mb-4">User Information</h2>
      <div className="grid grid-cols-1 gap-4">
        <input
          type="text"
          placeholder="First Name"
          className="input input-bordered w-full"
          value={preferences.first_name}
          onChange={e => setPreferences({ ...preferences, first_name: e.target.value })}
          required
        />
        <textarea
          placeholder="User Profile"
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
          <option value="">Select Timezone</option>
          {timezones.map(tz => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Persona</h2>
      <PersonaSelection selectedPersona={preferences.persona} onSelectPersona={handlePersonaSelect} />
      <div className="grid grid-cols-2 gap-4 mt-4">
        <input
          type="text"
          placeholder="Persona Name"
          className="input input-bordered w-full"
          value={preferences.persona}
          onChange={e => setPreferences({ ...preferences, persona: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Tone"
          className="input input-bordered w-full"
          value={preferences.tone}
          onChange={e => setPreferences({ ...preferences, tone: e.target.value })}
          required
        />
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Voice</h2>
      <VoiceSelection selectedVoice={preferences.voice} setSelectedVoice={(voice) => setPreferences({ ...preferences, voice })} />

      <h2 className="text-2xl font-bold mt-8 mb-4">Set Schedule</h2>
      <ScheduleForm schedule={schedule} setSchedule={setSchedule} />

      <button type="submit" className="btn btn-primary mt-8">
        Save Preferences
      </button>
    </form>
  );
}

export default PreferencesForm;