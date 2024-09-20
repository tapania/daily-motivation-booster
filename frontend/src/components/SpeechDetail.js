// frontend/src/components/SpeechDetail.js

import React, { useEffect, useState, useContext } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import API from '../api';
import { handleError } from '../utils/errorHandler';
import { AuthContext } from '../context/AuthContext';

function SpeechDetail({ type }) {
  const { id } = useParams();
  const { isAuthenticated } = useContext(AuthContext);
  const [speech, setSpeech] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSpeech = async () => {
      try {
        let endpoint = '';
        if (type === 'public') {
          endpoint = `/public_speeches/${id}/`;
        } else if (type === 'private') {
          if (!isAuthenticated) {
            setError('You must be logged in to view this speech.');
            setLoading(false);
            return;
          }
          endpoint = `/my_speeches/${id}/`;
        } else {
          setError('Invalid speech type.');
          setLoading(false);
          return;
        }

        const response = await API.get(endpoint);
        setSpeech(response.data);
      } catch (error) {
        handleError(error);
        if (error.response && error.response.status === 404) {
          setError('Speech not found.');
        } else {
          setError('Failed to load the speech.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchSpeech();
  }, [id, type, isAuthenticated]);

  if (loading) {
    return <div className="text-center mt-10">Loading speech details...</div>;
  }

  if (error) {
    return (
      <div className="text-center mt-10 text-red-500">
        {error}
        {type === 'private' && !isAuthenticated && <Navigate to="/" replace />}
      </div>
    );
  }

  if (!speech) {
    return <div className="text-center mt-10">Speech not found.</div>;
  }

  return (
    <div className="max-w-3xl mx-auto mt-8 p-6 border rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-4">{speech.title || 'Untitled Speech'}</h2>
      <p className="mb-4">{speech.speech_text}</p>
      {speech.speech_url && (
        <audio controls src={speech.speech_url} className="w-full mt-2"></audio>
      )}
      {/* Additional Details */}
      {type === 'public' && (
        <div className="mt-4">
          <span className="font-semibold">Created By:</span> {speech.creator_name || 'Unknown'}
        </div>
      )}
    </div>
  );
}

export default SpeechDetail;