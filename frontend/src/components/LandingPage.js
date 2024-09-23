// frontend/src/components/LandingPage.js

import React from 'react';
import { Link } from 'react-router-dom';
import PublicSpeeches from './PublicSpeeches';
import slide1 from '../assets/images/slide1.jpg';
import slide2 from '../assets/images/slide2.jpg';
import slide3 from '../assets/images/slide3.jpg';
import slide4 from '../assets/images/slide4.jpg';

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-start min-h-screen w-full text-black dark:text-white px-4 py-8 bg-white dark:bg-gray-900">
      {/* Logo and Tagline */}
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold mb-4">AlgorithmSpeaks</h1>
        <p className="text-2xl italic">Boost Your Ambitions with a Digital Push!</p>
      </div>

      {/* Slide Images Carousel */}
      <div className="carousel w-full max-w-4xl mb-8">
        <div id="slide1" className="carousel-item relative w-full">
          <img src={slide1} className="w-full" alt="Introduction" />
        </div>
        <div id="slide2" className="carousel-item relative w-full">
          <img src={slide2} className="w-full" alt="Personal Motivation" />
        </div>
        <div id="slide3" className="carousel-item relative w-full">
          <img src={slide3} className="w-full" alt="Key Features" />
        </div>
        <div id="slide4" className="carousel-item relative w-full">
          <img src={slide4} className="w-full" alt="Join Us" />
        </div>
      </div>

      {/* Navigation Buttons for Carousel */}
      <div className="flex justify-center w-full py-2 gap-2 mb-8">
        <a href="#slide1" className="btn btn-xs">1</a>
        <a href="#slide2" className="btn btn-xs">2</a>
        <a href="#slide3" className="btn btn-xs">3</a>
        <a href="#slide4" className="btn btn-xs">4</a>
      </div>

      {/* Disclaimer Section */}
      <div className="alert alert-warning shadow-lg max-w-3xl mb-8 bg-yellow-100 dark:bg-yellow-800 text-yellow-700 dark:text-yellow-200">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current flex-shrink-0 h-6 w-6 text-yellow-700 dark:text-yellow-200" fill="none" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01"></path>
          </svg>
          <span>
            <strong>Privacy Notice:</strong> Please do not include any personal or sensitive information in your profile. Instead, provide general directions or goals to help us tailor your motivational experience.
          </span>
        </div>
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
      <div className="max-w-3xl text-center text-sm italic text-gray-800 dark:text-gray-200">
        <p>
          🚧 Please note: This is a Hackathon project and some features might still be in development. We're working hard to bring you the best experience, but things might not be 100% polished just yet.
        </p>
        <p className="mt-2">
          ⚠️ We don't guarantee the delivery of speeches as the Azure credits budget for this project may run out if there's a surge in users. Thanks for understanding!
        </p>
      </div>

      {/* Spacer */}
      <div className="w-full border-t border-gray-300 dark:border-gray-700 my-12"></div>

      {/* Public Speeches Showcase */}
      <div className="w-full">
        <PublicSpeeches />
      </div>
    </div>
  );
}

export default LandingPage;