// src/components/MySpeeches.js
import React, { useEffect, useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import SpeechForm from './SpeechForm';
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';

function MySpeeches() {
  const { user } = useContext(AuthContext);
  const [speeches, setSpeeches] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMySpeeches = async () => {
      try {
        const response = await API.get('/my_speeches/');
        setSpeeches(response.data);
      } catch (error) {
        handleError(error);
        setError('Failed to load your speeches.');
      } finally {
        setLoading(false);
      }
    };

    fetchMySpeeches();
  }, []);

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

  if (loading) {
    return <div className="text-center mt-10">Loading your speeches...</div>;
  }

  return (
    <div className="mt-8">
      <h2 className="text-3xl font-bold mb-4">Your Personal Speeches</h2>

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
      {/* Speeches List with Collapsible Panels */}
      <div className="space-y-4">
        {speeches.length === 0 ? (
          <p>You haven't generated any speeches yet. Let's create one! 🎤</p>
        ) : (
          speeches.map((speech) => (
            <div key={speech.id} className="border rounded-lg">
              <details className="group">
                <summary className="flex justify-between items-center p-4 cursor-pointer bg-gray-100">
                  <span className="font-semibold">{speech.title || `${speech.speech_text.substring(0, 50)}...`}</span>
                  <svg
                    className="w-5 h-5 transition-transform duration-200 transform group-open:rotate-180"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </summary>
                <div className="p-4">
                  <p className="mb-2">{speech.speech_text}</p>
                  {speech.speech_url && (
                    <audio controls src={speech.speech_url} className="w-full mt-2"></audio>
                  )}
                  <Link
                    to={`/my_speeches/${speech.id}`}
                    className="text-blue-500 underline mt-2 inline-block"
                  >
                    View Details
                  </Link>
                </div>
              </details>
            </div>
          ))
        )}
      </div>

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
              <li><strong>User Profile:</strong> Give us a glimpse into who you are to tailor the speech. You can use <a href="https://copilot.microsoft.com" target="_blank" rel="noopener noreferrer">Copilot</a> to create the profile for you.</li>
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