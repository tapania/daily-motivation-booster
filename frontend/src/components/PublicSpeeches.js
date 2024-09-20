// src/components/PublicSpeeches.js
import React, { useEffect, useState, useContext } from 'react';
import { Link } from 'react-router-dom'; // Import Link for navigation
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';
import SpeechForm from './SpeechForm'; // Ensure SpeechForm is imported
import { personas } from '../personas';

function PublicSpeeches() {
  const { isAuthenticated } = useContext(AuthContext);
  const [speeches, setSpeeches] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch public speeches
    const fetchPublicSpeeches = async () => {
      try {
        const response = await API.get('/public_speeches/');
        setSpeeches(response.data);
      } catch (error) {
        handleError(error);
        setError('Failed to load public speeches.');
      } finally {
        setLoading(false);
      }
    };

    fetchPublicSpeeches();
  }, []);

  /**
   * Handles the submission of the public speech form.
   * @param {Object} formData - The data from the SpeechForm.
   */
  const handleGenerate = async (formData) => {
    setError('');
    setMessage('');
    try {
      const response = await API.post('/generate_public_speech', formData);
      setMessage('Public speech generated successfully! 🎉');
      // Fetch updated public speeches
      const speechesResponse = await API.get('/public_speeches/');
      setSpeeches(speechesResponse.data);
    } catch (error) {
      handleError(error);
      setError('An error occurred while generating the public speech.');
    }
  };

  if (loading) {
    return <div className="text-center mt-10">Loading public speeches...</div>;
  }

  return (
    <div className="mt-8">
      <h2 className="text-3xl font-bold mb-4">Public Speeches</h2>

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
          <p>No public speeches available at the moment.</p>
        ) : (
          speeches.map(speech => (
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
                  <pre className="mb-2">{speech.speech_text}</pre>
                  {speech.speech_url && (
                    <audio controls src={speech.speech_url} className="w-full mt-2"></audio>
                  )}
                </div>
              </details>
            </div>
          ))
        )}
      </div>

      {/* Generate New Public Speech Form - Visible Only to Authenticated Users */}
      {isAuthenticated ? (
        <div className="mt-8">
          <SpeechForm
            initialData={{
              first_name: '',
              user_profile: '',
              persona: '',
              tone: '',
              voice: '',
            }}
            onSubmit={handleGenerate}
            buttonText="Generate Public Speech 🚀"
            formTitle="Generate a Public Speech"
            instructions={
              <p>
                Ready to share some motivation with the world? Here's how to craft a public speech that resonates:
                <ol className="list-decimal list-inside mt-2">
                  <li><strong>First Name:</strong> Add your name to make the speech authentically yours.</li>
                  <li><strong>User Profile:</strong> Let us understand your background to personalize your message.</li>
                  <li><strong>Persona & Tone:</strong> Enter the name of your motivational speaker and describe their unique style.</li>
                  <li><strong>Voice:</strong> Select a voice that best conveys your motivational energy.</li>
                </ol>
                Hit "Generate Public Speech" and inspire your audience! ✨
              </p>
            }
          />
        </div>
      ) : (
        <div className="mt-8 p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
          <p>
            <strong>Want to generate a public speech?</strong> Please{' '}
            <a href={`${process.env.REACT_APP_BACKEND_URL}/login`} className="text-blue-500 underline">
              log in
            </a>{' '}
            using a Microsoft account to access this feature.
          </p>
        </div>
      )}
    </div>
  );
}

export default PublicSpeeches;