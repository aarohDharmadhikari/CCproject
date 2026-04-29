import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Canvas from './components/Canvas';
import Labs from './components/Labs';
import SavedArchitectures from './components/SavedArchitectures';
import './index.css';

function App() {
  const [selectedLab, setSelectedLab] = useState(null);
  const [architectureToLoad, setArchitectureToLoad] = useState(null);

  return (
    <Router>
      <div className="flex bg-primary text-white">
        <Sidebar />
        <main className="flex-1 p-4">
          <Routes>
            <Route 
              path="/" 
              element={
                <Canvas 
                  selectedLab={selectedLab} 
                  setSelectedLab={setSelectedLab} 
                  architectureToLoad={architectureToLoad}
                  setArchitectureToLoad={setArchitectureToLoad}
                />
              } 
            />
            <Route path="/labs" element={<Labs setSelectedLab={setSelectedLab} />} />
            <Route 
              path="/saved" 
              element={
                <SavedArchitectures 
                  setArchitectureToLoad={setArchitectureToLoad} 
                />
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
