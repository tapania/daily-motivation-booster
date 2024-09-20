// src/components/PublicSpeeches.js
import React, { useEffect, useState, useContext } from 'react';
import SpeechForm from './SpeechForm'; // New import
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';
import { personas } from '../personas';

function PublicSpeeches() {
  const { isAuthenticated } = useContext(AuthContext);
  const [speeches, setSpeeches] = useState([]);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch public speeches
    const fetchPublicSpeeches = async () => {
      try {
        const response = await API.get('/public_speeches/');
        setSpeeches(response.data);
      } catch (error) {
        handleError(error);
        setError('Failed to load public speeches.');
      }
    };



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

      {/* Speeches List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {speeches.map(speech => (
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
