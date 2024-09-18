// frontend/src/components/PublicSpeeches.js
import React, { useEffect, useState } from 'react';
import API from '../api';
import { handleError } from '../utils/errorHandler';

function PublicSpeeches() {
  const [speeches, setSpeeches] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [speechUrl, setSpeechUrl] = useState(null);
  const [formData, setFormData] = useState({
    first_name: '',
    user_profile: '',
    persona: '',
    tone: '',
    voice: '',
  });
  const [voices, setVoices] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch public speeches
    API.get('/public_speeches/')
      .then(response => setSpeeches(response.data.speeches))
      .catch(error => handleError(error));

    // Fetch available voices
    API.get('/voices/')
      .then(response => setVoices(response.data.voices))
      .catch(error => handleError(error));
  }, []);

  const handleGenerate = () => {
    setGenerating(true);
    API.post('/generate_speech', formData)
      .then(response => {
        setSpeechUrl(response.data.speech_url);
        setGenerating(false);
      })
      .catch(error => {
        handleError(error);
        setMessage('An error occurred while generating the speech.');
        setGenerating(false);
      });
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Public Speeches</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {speeches.map((url, index) => (
          <div key={index} className="card shadow-md p-4">
            <audio controls src={url} className="w-full"></audio>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Generate a One-Time Speech</h2>
        <div className="grid grid-cols-1 gap-4">
          <input
            type="text"
            placeholder="First Name"
            className="input input-bordered w-full"
            value={formData.first_name}
            onChange={e => setFormData({ ...formData, first_name: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="User Profile"
            className="input input-bordered w-full"
            value={formData.user_profile}
            onChange={e => setFormData({ ...formData, user_profile: e.target.value })}
          />
          <input
            type="text"
            placeholder="Persona"
            className="input input-bordered w-full"
            value={formData.persona}
            onChange={e => setFormData({ ...formData, persona: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Tone"
            className="input input-bordered w-full"
            value={formData.tone}
            onChange={e => setFormData({ ...formData, tone: e.target.value })}
            required
          />
          <select
            className="select select-bordered w-full"
            value={formData.voice}
            onChange={e => setFormData({ ...formData, voice: e.target.value })}
            required
          >
            <option value="">Select a Voice</option>
            {voices.map(voice => (
              <option key={voice} value={voice}>
                {voice}
              </option>
            ))}
          </select>
          <button
            onClick={handleGenerate}
            className={`btn btn-primary ${generating ? 'loading' : ''}`}
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate Speech'}
          </button>
          {speechUrl && (
            <div className="mt-4">
              <h3 className="text-xl font-bold">Your Speech</h3>
              <audio controls src={speechUrl} className="w-full mt-2"></audio>
            </div>
          )}
          {message && <p className="text-red-500">{message}</p>}
        </div>
      </div>
    </div>
  );
}

export default PublicSpeeches;