// src/components/SpeechForm.js
import React, { useState, useEffect } from 'react';
import PersonaSelection from './PersonaSelection';
import VoiceSelection from './VoiceSelection';
import { personas } from '../personas';

/**
 * Reusable SpeechForm component for generating speeches.
 *
 * Props:
 * - initialData: Object containing initial form values.
 * - onSubmit: Function to handle form submission.
 * - buttonText: String for the submit button text.
 * - formTitle: String for the form's title.
 * - instructions: JSX or string for additional instructions.
 */
function SpeechForm({ initialData = {}, onSubmit, buttonText = 'Generate Speech', formTitle = 'Generate a Speech', instructions }) {
  const [formData, setFormData] = useState({
    first_name: '',
    user_profile: '',
    persona: '',
    tone: '',
    voice: '',
    ...initialData,
  });
  const [voicesList, setVoicesList] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Fetch available voices when the component mounts
    const fetchVoices = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/voices/`, {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch voices.');
        }
        const data = await response.json();
        setVoicesList(data.voices);
      } catch (err) {
        console.error(err);
        setError('Failed to load available voices.');
      }
    };

    fetchVoices();
  }, []);

  /**
   * Handles persona selection and updates the corresponding tone.
   * @param {string} personaName - The selected persona name.
   */
  const handlePersonaSelect = (personaName) => {
    const selected = personas.find(p => p.name === personaName);
    if (selected) {
      setFormData(prevData => ({
        ...prevData,
        persona: selected.name,
        tone: selected.tone,
      }));
    }
  };

  /**
   * Handles form submission.
   * @param {Event} e - The form submission event.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setGenerating(true);
    setError('');
    setMessage('');

    try {
      await onSubmit(formData);
      setMessage('Speech generated successfully! 🚀');
      // Optionally reset form fields if needed
      // setFormData({
      //   first_name: '',
      //   user_profile: '',
      //   persona: '',
      //   tone: '',
      //   voice: '',
      // });
    } catch (err) {
      console.error(err);
      setError('An error occurred while generating the speech.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="mt-8">
      {formTitle && <h2 className="text-3xl font-bold mb-4">{formTitle}</h2>}
      
      {/* Instructions Pane */}
      {instructions && (
        <div className="collapse collapse-arrow border border-base-300 bg-base-100 rounded-box mb-6">
          <input type="checkbox" />
          <div className="collapse-title text-xl font-medium">
            Need Help Filling Out the Form?
          </div>
          <div className="collapse-content">
            {instructions}
          </div>
        </div>
      )}

      {/* Display Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      {/* Display Success Message */}
      {message && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
        <input
          type="text"
          placeholder="🚀 Your First Name"
          className="input input-bordered w-full"
          value={formData.first_name}
          onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
          required
        />
        <textarea
          placeholder="📝 Tell us about yourself..."
          className="textarea textarea-bordered w-full"
          value={formData.user_profile}
          onChange={(e) => setFormData({ ...formData, user_profile: e.target.value })}
          rows={4}
        ></textarea>

        <PersonaSelection selectedPersona={formData.persona} onSelectPersona={handlePersonaSelect} />

        <input
          type="text"
          placeholder="🎤 Persona Name (e.g., Coach Carter)"
          className="input input-bordered w-full"
          value={formData.persona}
          onChange={(e) => setFormData({ ...formData, persona: e.target.value })}
          required
        />
        <textarea
          placeholder="🗣️ Tone Description (e.g., Energetic and Persuasive)"
          className="textarea textarea-bordered w-full"
          value={formData.tone}
          onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
          rows={4}
          required
        ></textarea>
        
        <VoiceSelection
          selectedVoice={formData.voice}
          setSelectedVoice={(voice) => setFormData({ ...formData, voice })}
        />

        <button
          type="submit"
          className={`btn btn-primary ${generating ? 'loading' : ''}`}
          disabled={generating}
        >
          {generating ? 'Cranking Up the Energy...' : buttonText}
        </button>
      </form>
    </div>
  );
}

export default SpeechForm;