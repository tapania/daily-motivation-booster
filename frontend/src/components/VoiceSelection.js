// src/components/VoiceSelection.js
import React, { useEffect, useState } from 'react';
import API from '../api';
import { handleError } from '../utils/errorHandler';

function VoiceSelection({ selectedVoice, setSelectedVoice }) {
  const [voices, setVoices] = useState([]);

  useEffect(() => {
    API.get('/voices/')
      .then(response => setVoices(response.data.voices))
      .catch(error => handleError(error));
  }, []);

  return (
    <select
      className="select select-bordered w-full"
      value={selectedVoice}
      onChange={e => setSelectedVoice(e.target.value)}
    >
      <option value="">Select a Voice</option>
      {voices.map(voice => (
        <option key={voice} value={voice}>
          {voice}
        </option>
      ))}
    </select>
  );
}

export default VoiceSelection;