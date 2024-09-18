// frontend/src/components/MySpeeches.js
import React, { useEffect, useState, useContext } from 'react';
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';

function MySpeeches() {
  const { user } = useContext(AuthContext);
  const [speeches, setSpeeches] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    first_name: user.first_name || '',
    user_profile: user.user_profile || '',
    persona: user.preferences?.persona || '',
    tone: user.preferences?.tone || '',
    voice: user.preferences?.voice || '',
  });
  const [voicesList, setVoicesList] = useState([]);

  useEffect(() => {
    const fetchMySpeeches = async () => {
      try {
        const response = await API.get('/my_speeches/');
        setSpeeches(response.data);
      } catch (error) {
        handleError(error);
        setError('Failed to load your speeches.');
      }
    };

    const fetchVoices = async () => {
      try {
        const response = await API.get('/voices/');
        setVoicesList(response.data.voices);
      } catch (error) {
        handleError(error);
        setError('Failed to load available voices.');
      }
    };

    fetchMySpeeches();
    fetchVoices();
  }, []);

  const handleGenerate = async (e) => {
    e.preventDefault();
    setGenerating(true);
    setError('');
    setMessage('');
    try {
      const response = await API.post('/generate_speech', formData);
      setMessage('Speech generated successfully!');
      setFormData({
        ...formData,
        first_name: user.first_name, // Assuming first name is not changing
        user_profile: user.user_profile,
        persona: user.preferences?.persona || '',
        tone: user.preferences?.tone || '',
        voice: user.preferences?.voice || '',
      });
      // Fetch updated speeches
      const speechesResponse = await API.get('/my_speeches/');
      setSpeeches(speechesResponse.data);
    } catch (error) {
      handleError(error);
      setError('An error occurred while generating the speech.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">My Speeches</h2>
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
      {speeches.length === 0 ? (
        <p>You have not generated any speeches yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {speeches.map((speech) => (
            <div key={speech.id} className="card shadow-md p-4">
              <h3 className="font-bold mb-2">{speech.speech_text.substring(0, 50)}...</h3>
              <audio controls src={speech.speech_url} className="w-full"></audio>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Generate a New Speech</h2>
        <form onSubmit={handleGenerate} className="grid grid-cols-1 gap-4">
          <input
            type="text"
            placeholder="First Name"
            className="input input-bordered w-full"
            value={formData.first_name}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
            required
          />
          <textarea
            placeholder="User Profile"
            className="textarea textarea-bordered w-full"
            value={formData.user_profile}
            onChange={(e) => setFormData({ ...formData, user_profile: e.target.value })}
            rows={4}
          ></textarea>
          <input
            type="text"
            placeholder="Persona"
            className="input input-bordered w-full"
            value={formData.persona}
            onChange={(e) => setFormData({ ...formData, persona: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Tone"
            className="input input-bordered w-full"
            value={formData.tone}
            onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
            required
          />
          <select
            className="select select-bordered w-full"
            value={formData.voice}
            onChange={(e) => setFormData({ ...formData, voice: e.target.value })}
            required
          >
            <option value="">Select a Voice</option>
            {voicesList.map((voice) => (
              <option key={voice} value={voice}>
                {voice}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className={`btn btn-primary ${generating ? 'loading' : ''}`}
            disabled={generating}
          >
            {generating ? 'Generating...' : 'Generate Speech'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default MySpeeches;