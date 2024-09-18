// frontend/src/components/PreferencesForm.js
import React, { useState, useEffect } from 'react';
import PersonaSelection from './PersonaSelection';
import VoiceSelection from './VoiceSelection';
import ScheduleForm from './ScheduleForm';
import API from '../api';
import { handleError } from '../utils/errorHandler';

function PreferencesForm() {
  const [user, setUser] = useState(null);
  const [preferences, setPreferences] = useState({
    persona: '',
    tone: '',
    voice: '',
  });
  const [schedule, setSchedule] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await API.get('/me');
        setUser(response.data);
      } catch (error) {
        handleError(error);
      }
    };

    fetchUser();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Update preferences
      await API.post('/preferences/', preferences);
      // Update schedule
      await API.post('/schedule/', schedule);
      setMessage('Preferences saved successfully!');
    } catch (error) {
      handleError(error);
      setMessage('An error occurred while saving your preferences.');
    }
  };

  if (!user) {
    return <div>Loading user information...</div>;
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">User Information</h2>
      <div className="grid grid-cols-1 gap-4">
        <input
          type="text"
          placeholder="First Name"
          className="input input-bordered w-full"
          value={user.first_name}
          readOnly
        />
        <input
          type="text"
          placeholder="User Profile"
          className="input input-bordered w-full"
          value={user.user_profile || ''}
          onChange={e => setUser({ ...user, user_profile: e.target.value })}
        />
        <input
          type="text"
          placeholder="Timezone"
          className="input input-bordered w-full"
          value={user.timezone}
          onChange={e => setUser({ ...user, timezone: e.target.value })}
          required
        />
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Persona</h2>
      <PersonaSelection selectedPersona={preferences.persona} setSelectedPersona={(persona) => setPreferences({ ...preferences, persona, tone: getTone(persona) })} />

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Voice</h2>
      <VoiceSelection selectedVoice={preferences.voice} setSelectedVoice={(voice) => setPreferences({ ...preferences, voice })} />

      <h2 className="text-2xl font-bold mt-8 mb-4">Set Schedule</h2>
      <ScheduleForm schedule={schedule} setSchedule={setSchedule} />

      <button type="submit" className="btn btn-primary mt-8">
        Save Preferences
      </button>
      {message && <p className="mt-4">{message}</p>}
    </form>
  );
}

// Helper function to get tone based on persona
const getTone = (persona) => {
  const personas = [
    { name: "Coach Carter", tone: "Inspirational" },
    { name: "Serene Monk", tone: "Calm and Reflective" },
    { name: "Drill Sergeant", tone: "Tough Love" },
    { name: "Cheerful Friend", tone: "Friendly and Upbeat" },
    { name: "Visionary Leader", tone: "Forward-thinking" },
    { name: "Wise Elder", tone: "Nurturing Wisdom" },
    { name: "Motivational Speaker", tone: "Energetic and Persuasive" },
    { name: "Empathetic Listener", tone: "Understanding and Comforting" },
  ];

  const selected = personas.find(p => p.name === persona);
  return selected ? selected.tone : '';
};

export default PreferencesForm;