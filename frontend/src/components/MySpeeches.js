// src/components/MySpeeches.js
import React, { useEffect, useState, useContext } from 'react';
import SpeechForm from './SpeechForm'; // New import
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';

function MySpeeches() {
  const { user } = useContext(AuthContext);
  const [speeches, setSpeeches] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');


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


  /**
   * Handles the submission of the speech form.
   * @param {Object} formData - The data from the SpeechForm.
   */
  const handleGenerate = async (formData) => {
    setError('');
    setMessage('');
    try {
      const response = await API.post('/generate_speech', formData);
      setMessage('Speech generated successfully! 🚀');
      // Fetch updated speeches
      const speechesResponse = await API.get('/my_speeches/');
      setSpeeches(speechesResponse.data);
    } catch (error) {
      handleError(error);
      setError('An error occurred while generating the speech.');
    }
  };

  if (!user) {
    return <div className="text-center mt-10">Loading user information...</div>;
  }

  return (
    <div className="mt-8">
      <h2 className="text-3xl font-bold mb-4">Your Personal Speeches</h2>

      {/* Instructions Pane */}
      <div className="collapse collapse-arrow border border-base-300 bg-base-100 rounded-box mb-6">
        <input type="checkbox" />
        <div className="collapse-title text-xl font-medium">
          Need a Hand Generating Your Speech?
        </div>
        <div className="collapse-content">
          <p className="mt-2">
            Hey, superstar! Ready to craft your next motivational masterpiece? Here's how:
          </p>
          <ol className="list-decimal list-inside mt-2">
            <li><strong>First Name:</strong> Personalize your speech by adding your name.</li>
            <li><strong>User Profile:</strong> Give us a glimpse into who you are to tailor the speech.</li>
            <li><strong>Persona & Tone:</strong> Enter the name of your motivational speaker and describe their unique style.</li>
            <li><strong>Voice:</strong> Choose a voice that pumps you up the most.</li>
          </ol>
          <p className="mt-2">Once you're set, hit that "Generate Speech" button and watch the magic happen! ✨</p>
        </div>
      </div>

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
      {/* Speeches List */}
      {speeches.length === 0 ? (
        <p>You haven't generated any speeches yet. Let's create one! 🎤</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {speeches.map((speech) => (
            <div key={speech.id} className="card shadow-md p-4">
              <h3 className="font-bold mb-2">
                {speech.speech_text.length > 50
                  ? `${speech.speech_text.substring(0, 50)}...`
                  : speech.speech_text}
              </h3>
              <audio controls src={speech.speech_url} className="w-full mt-2"></audio>
            </div>
          ))}
        </div>
      )}

      {/* Generate New Speech Form */}
      <SpeechForm
        initialData={{
          first_name: user.first_name || '',
          user_profile: user.user_profile || '',
          persona: user.preferences?.persona || '',
          tone: user.preferences?.tone || '',
          voice: user.preferences?.voice || '',
        }}
        onSubmit={handleGenerate}
        buttonText="Generate Your Boost! 🚀"
        formTitle="Generate a New Speech"
        instructions={
          <p>
            Hey, superstar! Ready to craft your next motivational masterpiece? Here's how:
            <ol className="list-decimal list-inside mt-2">
              <li><strong>First Name:</strong> Personalize your speech by adding your name.</li>
              <li><strong>User Profile:</strong> Give us a glimpse into who you are to tailor the speech.</li>
              <li><strong>Persona & Tone:</strong> Enter the name of your motivational speaker and describe their unique style.</li>
              <li><strong>Voice:</strong> Choose a voice that pumps you up the most.</li>
            </ol>
            Once you're set, hit that "Generate Speech" button and watch the magic happen! ✨
          </p>
        }
      />
    </div>
  );
}

export default MySpeeches;