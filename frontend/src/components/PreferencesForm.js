// src/components/PreferencesForm.js
import React, { useState } from 'react';
import PersonaSelection from './PersonaSelection';
import VoiceSelection from './VoiceSelection';
import ScheduleForm from './ScheduleForm';
import API from '../api';
import { handleError } from '../utils/errorHandler';

function PreferencesForm() {
  const [firstName, setFirstName] = useState('');
  const [userProfile, setUserProfile] = useState('');
  const [timezone, setTimezone] = useState('UTC');
  const [selectedPersona, setSelectedPersona] = useState('');
  const [selectedVoice, setSelectedVoice] = useState('');
  const [schedule, setSchedule] = useState([]);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Update preferences
      await API.post('/preferences/', {
        persona: selectedPersona,
        tone: selectedPersona.tone,
        voice: selectedVoice,
      });
      // Update schedule
      await API.post('/schedule/', schedule);
      setMessage('Preferences saved successfully!');
    } catch (error) {
      handleError(error);
      setMessage('An error occurred while saving your preferences.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">User Information</h2>
      <div className="grid grid-cols-1 gap-4">
        <input
          type="text"
          placeholder="First Name"
          className="input input-bordered w-full"
          value={firstName}
          onChange={e => setFirstName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="User Profile"
          className="input input-bordered w-full"
          value={userProfile}
          onChange={e => setUserProfile(e.target.value)}
        />
        <input
          type="text"
          placeholder="Timezone"
          className="input input-bordered w-full"
          value={timezone}
          onChange={e => setTimezone(e.target.value)}
          required
        />
      </div>

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Persona</h2>
      <PersonaSelection selectedPersona={selectedPersona} setSelectedPersona={setSelectedPersona} />

      <h2 className="text-2xl font-bold mt-8 mb-4">Select Voice</h2>
      <VoiceSelection selectedVoice={selectedVoice} setSelectedVoice={setSelectedVoice} />

      <h2 className="text-2xl font-bold mt-8 mb-4">Set Schedule</h2>
      <ScheduleForm schedule={schedule} setSchedule={setSchedule} />

      <button type="submit" className="btn btn-primary mt-8">
        Save Preferences
      </button>
      {message && <p className="mt-4">{message}</p>}
    </form>
  );
}

export default PreferencesForm;
