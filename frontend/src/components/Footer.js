// src/components/Footer.js
import React from 'react';

function Footer() {
  return (
    <footer className="footer p-4 bg-neutral text-neutral-content">
      <div className="container mx-auto text-center">
        <p>© {new Date().getFullYear()} Motivational Speech App. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
