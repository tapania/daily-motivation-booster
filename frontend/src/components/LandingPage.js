// src/components/LandingPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import PublicSpeeches from './PublicSpeeches';

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-start min-h-screen text-black px-4 py-8">
      {/* Logo and Tagline */}
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold mb-4">AlgorithmSpeaks</h1>
        <p className="text-2xl italic">Boost Your Ambitions with a Digital Push!</p>
      </div>

      {/* Description */}
      <div className="max-w-3xl text-center mb-8">
        <p className="mb-4">
          Hey there, superstar! Welcome to <strong>AlgorithmSpeaks</strong>—your go-to hub for crafting personalized motivational speeches that keep you charged up and ready to conquer any challenge. 🚀
        </p>
        <p className="mb-4">
          Whether you're an engineer debugging your daily tasks, a salesperson closing those deals, or a creative mind brainstorming the next big idea, we've got your back with tailored encouragement that fits your unique hustle. 💼✨
        </p>
      </div>

      {/* Features Overview */}
      <div className="max-w-3xl text-left mb-8">
        <h2 className="text-3xl font-semibold mb-4">What We Offer</h2>
        <ul className="list-disc list-inside space-y-2">
          <li><strong>Create:</strong> Generate motivational speeches that resonate with your personal and professional journey.</li>
          <li><strong>Schedule:</strong> Plan your motivational boosts to arrive precisely when you need them.</li>
          <li><strong>Personalize:</strong> Customize your experience with different personas and tones to match your style.</li>
        </ul>
      </div>

      {/* Call to Action */}
      <div className="mb-12">
        <a
          href={`${process.env.REACT_APP_BACKEND_URL}/login`}
          className="btn btn-primary btn-lg"
        >
          🚀 Get Started with Microsoft Login
        </a>
      </div>

      {/* Disclaimers */}
      <div className="max-w-3xl text-center text-sm italic text-gray-200">
        <p>
          🚧 Please note: This is a Hackathon project and some features might still be in development. We're working hard to bring you the best experience, but things might not be 100% polished just yet.
        </p>
        <p className="mt-2">
          ⚠️ We don't guarantee the delivery of speeches as the Azure credits budget for this project may run out if there's a surge in users. Thanks for understanding!
        </p>
      </div>

      {/* Spacer */}
      <div className="w-full border-t border-gray-300 my-12"></div>

      {/* Public Speeches Showcase */}
      <div className="w-full">
        <PublicSpeeches />
      </div>
    </div>
  );
}

export default LandingPage;
