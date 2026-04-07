//* ************************************************************************************************
// * Date: August 10th 2022           |*************************************************************
// * Last Updated: Febuary 13th 2025  |*************************************************************
// *************************************************************************************************
// ********************************#* Description: |************************************************
// <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>|
// | This is the Navbar component for the Zencrypt application. This component is responsible for  |
// | rendering the navigation bar at the top of the application. The navigation bar contains links |
// | to the different pages of the application. The Navbar component is a functional component that|
// | returns the JSX for the navigation bar.                                                       |
// |********************************************************************************************** |
// | The Navbar component is imported into the App component and rendered at the top of the        |
// | application. The navigation bar contains links to the different pages of the application.     |
// | The navigation bar is styled using Tailwind CSS classes.                                      |
// |***********************************************************************************************|
// <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>|
// *************************************************************************************************

import React from 'react';
import ReactDOM from 'react-dom';

const Navbar = () => {
  return (
    <nav className="bg-black text-white p-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center">
          <div className="text-xl font-bold">Zencrypt v6.2-alpha</div>
          
          <div className="flex space-x-2">
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Hash</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Encrypt</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Decrypt</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">File Operations</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Advanced</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Export Key</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Import Key</button>
            <button className="px-2 py-1 bg-gray-800 hover:bg-gray-700 rounded">Logout</button>
          </div>
        </div>
        
        <div className="mt-2 text-sm text-gray-400">
          © 2025 All rights reserved by 
          <a href="https://imaclone.x" className="text-blue-400 hover:text-blue-300 ml-1">
            imaclone.x
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;