// src/components/Footer.js
import React from 'react';

function Footer() {
  return (
    <footer className="footer p-4 bg-neutral text-neutral-content">
      <div className="container mx-auto text-center">
        <p>© {new Date().getFullYear()} AlgorithmSpeaks.com. All rights reserved.</p>
        <p className="text-sm italic">Boost Your Ambitions with a Digital Push!</p>
      </div>
    </footer>
  );
}

export default Footer;
