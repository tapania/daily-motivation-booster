// frontend/src/components/Header.js
import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Header() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const location = useLocation();

  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="flex flex-col items-center md:items-start">
          <h1 className="text-xl font-bold">AlgorithmSpeaks</h1>
          <p className="text-sm italic">Boost Your Ambitions with a Digital Push!</p>
        </div>
        {isAuthenticated && (
          <nav className="mt-2 md:mt-0">
            <ul className="flex space-x-4">
              <li>
                <Link
                  to="/"
                  className={`hover:underline ${location.pathname === '/' ? 'underline' : ''}`}
                >
                  Public Speeches
                </Link>
              </li>
              <li>
                <Link
                  to="/my_speeches"
                  className={`hover:underline ${location.pathname === '/my_speeches' ? 'underline' : ''}`}
                >
                  My Speeches
                </Link>
              </li>
              <li>
                <Link
                  to="/settings"
                  className={`hover:underline ${location.pathname === '/settings' ? 'underline' : ''}`}
                >
                  Settings
                </Link>
              </li>
            </ul>
          </nav>
        )}
        <div className="mt-2 md:mt-0">
          {isAuthenticated ? (
            <button
              onClick={logout}
              className="btn btn-sm btn-outline btn-error"
            >
              Logout
            </button>
          ) : (
            <a
              href={`${process.env.REACT_APP_BACKEND_URL}/login`}
              className="btn btn-sm btn-outline btn-primary"
            >
              🚀 Login with Microsoft
            </a>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;