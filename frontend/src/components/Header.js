// frontend/src/components/Header.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Header({ isAuthenticated, handleLogout }) {
  const location = useLocation();

  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold">Motivational Speech App</h1>
        <nav>
          <ul className="flex space-x-4">
            <li>
              <Link
                to="/"
                className={`hover:underline ${location.pathname === '/' ? 'underline' : ''}`}
              >
                Public Speeches
              </Link>
            </li>
            {isAuthenticated && (
              <>
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
              </>
            )}
          </ul>
        </nav>
        <div>
          {isAuthenticated ? (
            <button
              onClick={handleLogout}
              className="btn btn-sm btn-outline btn-error"
            >
              Logout
            </button>
          ) : (
            <a
              href={`${process.env.REACT_APP_BACKEND_URL}/login`}
              className="btn btn-sm btn-outline btn-primary"
            >
              Login
            </a>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;