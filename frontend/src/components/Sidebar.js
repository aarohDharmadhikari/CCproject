import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  const navLinkClasses = ({ isActive }) =>
    `block py-2.5 px-4 rounded-lg transition-colors duration-200 ease-in-out ${
      isActive
        ? 'bg-accent text-primary font-semibold'
        : 'hover:bg-secondary'
    }`;

  return (
    <div className="w-64 bg-primary p-4 border-r border-gray-800 flex flex-col">
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-white">CloudLab</h1>
        <p className="text-gray-400 text-sm">Virtual Simulator</p>
      </div>
      <nav className="flex-grow">
        <ul>
          <li className="mb-4">
            <NavLink to="/" className={navLinkClasses}>
              Canvas
            </NavLink>
          </li>
          <li className="mb-4">
            <NavLink to="/labs" className={navLinkClasses}>
              Labs
            </NavLink>
          </li>
          <li className="mb-4">
            <NavLink to="/saved" className={navLinkClasses}>
              Saved Architectures
            </NavLink>
          </li>
        </ul>
      </nav>
      <div className="text-xs text-gray-600">
        <p>Version 2.0.0</p>
      </div>
    </div>
  );
};

export default Sidebar;
