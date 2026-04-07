// ********************************************************************************************
// * Title: Zencrypt WebApp           |********************************************************
// * Developed by: Ryan Hatch         |********************************************************
//   Date: August 10th 2022           |********************************************************
//   Last Updated: February 13th 2025 |********************************************************
//   Version: 6.2-A                   |********************************************************
// -  *****************************************************************************************
// *  ***************************#*| Zencrypt v6.2-A |*****************************************
// <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
// *******************************#* Description: |********************************************
// <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
// |              Zencrypt Web-App is a Flask application that can be used to:                |
// |       - Generate hashes: using SHA256 hashing algorithm, with an optional salt value.    |
// |       - Encrypt text and files: using Fernet symmetric encryption algorithm.             |
// <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

import React, { useState, useEffect } from 'react';
import { Alert, AlertTitle } from '@/components/ui/alert';
import { Lock, Mail, Key } from 'lucide-react';

//* ---------------------- | This component handles user authentication and PGP key generation for the user | ---------------------- *//

const AuthComponent = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);              // Check if user is authenticated or not
  const [user, setUser] = useState(null);                                    // Store user data if authenticated or logged in
  const [error, setError] = useState('');                                   // Store error messages if any error occurs during the either authentication or key generation
  const [keys, setKeys] = useState({ publicKey: null, privateKey: null }); // Store the PGP keys if the successfully were generated 

  useEffect(() => {                                    // Check if the user is already authenticated
                                                      // Check for existing JWT token
    const token = localStorage.getItem('jwt_token'); // Get the JWT token from the local storage if it exists or not
    if (token) {                                    // If the token exists, validate the token to check if it is still valid or not
      validateToken(token);                        // Validate the token by sending a request to the server
    }
  }, []);

  const validateToken = async (token) => {                   // Validate the JWT token by sending a request to the server
    try {                                                   // Try to validate the token
      const response = await fetch('/api/auth/validate', { // Send a request to the server to validate the token
        method: 'POST',                                   // Use the POST method to send the request
        headers: {                                       // Set the headers for the request
          'Authorization': `Bearer ${token}`,           // Set the Authorization header with the token
          'Content-Type': 'application/json'           // Set the Content-Type header with the value application/json
        }
      });
      if (response.ok) {                          // If the response is OK, then the token is valid and the user is authenticated
        const userData = await response.json();  // Parse the response data to get the user data from the server
        setUser(userData);                      // Set the user data in the state variable
        setIsAuthenticated(true);              // Set the isAuthenticated state variable to true
      } else {                                // If the response is not OK, then the token is invalid and the user is not authenticated
        localStorage.removeItem('jwt_token');// Remove the token from the local storage
        setIsAuthenticated(false);          // Set the isAuthenticated state variable to false
      }
    } catch (err) {                         // If an error occurs during the token validation process
      setError('Token validation failed'); // Set the error message to Token validation failed
    }
  };

//* ---------------------- | Generate PGP Keys For The User | ---------------------- *//

  const generatePGPKeys = async () => {                                        // Generate PGP keys for the user
    try {                                                                     // Try to generate the PGP keys
      const response = await fetch('/api/keys/generate', {                   // Send a request to the server to generate the PGP keys
        method: 'POST',                                                     // Use the POST method to send the request
        headers: {                                                         // Set the headers for the request
          'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Set the Authorization header with the JWT token
          'Content-Type': 'application/json'                             // Set the Content-Type header with the value application/json
        }
      });
      
      if (response.ok) {                        // Checks if the response is OK or not
        const keyData = await response.json(); // Parse the response data to get the PGP keys
        setKeys(keyData);                     // Set the PGP keys in the state variable
        
        // Store keys in MongoDB associated with user
        await fetch('/api/keys/store', { // Send a request to the server to store the PGP keys in the database
          method: 'POST',               // Use the POST method to send the request
          headers: {                   // Set the headers for the request
            'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`, // Set the Authorization header with the JWT token
            'Content-Type': 'application/json'                             // Set the Content-Type header with the value application/json
          },
          body: JSON.stringify({           // Set the body of the request with the user ID and the public key
            userId: user.id,              // Set the userId with the user ID
            publicKey: keyData.publicKey // Set the publicKey with the public key
          })
        });
      }
    } catch (err) {                             // If an error occurs during the PGP key generation process
      setError('Failed to generate PGP keys'); // Set the error message to Failed to generate PGP keys
    }
  };

//* ---------------------- | Logic For User Login | ---------------------- *//

  const handleLogin = async (email, password) => {        // Handle the user login process by sending a request to the server
    try {                                                // Try to login the user
      const response = await fetch('/api/auth/login', { // Send a request to the server to login the user
        method: 'POST',                                // Use the POST method to send the request
        headers: {                                    // Set the headers for the request
          'Content-Type': 'application/json'         // Set the Content-Type header with the value application/json
        },
        body: JSON.stringify({ email, password }) // Set the body of the request with the email and password
      });

      if (response.ok) {                                          // If the response is OK, then the user is successfully logged in
        const { token, user: userData } = await response.json(); // Parse the response data to get the JWT token and the user data
        localStorage.setItem('jwt_token', token);               // Store the JWT token in the local storage
        setUser(userData);                                     // Set the user data in the state variable
        setIsAuthenticated(true);                             // Set the isAuthenticated state variable to true
      } else {                                               // If the response is not OK, then the user login failed
        setError('Invalid credentials');                    // Set the error message to Invalid credentials
      }
    } catch (err) {                                       // If an error occurs during the user login process
      setError('Login failed');                          // Set the error message to Login failed
    }
  };

  return ( 

//* ---------------------- | JSX Structure For Authorization Page | ---------------------- *//
            
    <div className="w-full max-w-md mx-auto p-6">
      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertTitle>{error}</AlertTitle>
        </Alert>
      )}

      {!isAuthenticated ? (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-center">Login to Zencrypt</h2>
          <form onSubmit={(e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            handleLogin(formData.get('email'), formData.get('password'));
          }} className="space-y-4">
            <div className="flex items-center space-x-2">
              <Mail className="w-5 h-5" />
              <input
                type="email"
                name="email"
                placeholder="Email"
                className="w-full max-w-xs p-2 border rounded"
                required
              />
            </div>
            <div className="flex items-center space-x-2">
              <Lock className="w-5 h-5" />
              <input
                type="password"
                name="password"
                placeholder="Password"
                className="w-full max-w-xs p-2 border rounded"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
            >
              Login
            </button>
          </form>
        </div>
      ) : (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Welcome, {user?.email}</h2>
          {!keys.publicKey && (
            <button
              onClick={generatePGPKeys}
              className="flex items-center space-x-2 bg-green-600 text-white p-2 rounded hover:bg-green-700"
            >
              <Key className="w-5 h-5" />
              <span>Generate PGP Keys</span>
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AuthComponent;