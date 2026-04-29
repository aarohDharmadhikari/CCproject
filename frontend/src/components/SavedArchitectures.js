import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const SavedArchitectures = ({ setArchitectureToLoad }) => {
  const [architectures, setArchitectures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchArchitectures = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/architectures');
        setArchitectures(response.data);
      } catch (err) {
        setError('Failed to fetch saved architectures. Please ensure the backend is running and accessible.');
        // console.error(err); // Removed for final cleanup
      } finally {
        setLoading(false);
      }
    };
    fetchArchitectures();
  }, []);

  const handleLoadArchitecture = (architectureData) => {
    setArchitectureToLoad(architectureData);
    navigate('/'); // Navigate to the Canvas page
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full p-4">
        <svg className="animate-spin h-8 w-8 text-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p className="ml-3 text-lg text-gray-300">Loading saved architectures...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-4 text-red-500 bg-secondary rounded-lg shadow-lg border border-red-700">
        <p className="font-bold text-lg mb-2">Error:</p>
        <p>{error}</p>
        <p className="text-sm text-gray-400 mt-2">Please check your backend server and network connection.</p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h2 className="text-3xl font-bold mb-6 text-white">Saved Architectures</h2>
      {architectures.length === 0 ? (
        <p className="text-gray-400">No architectures saved yet. Start building on the Canvas!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {architectures.map((arch) => (
            <div key={arch.id} className="bg-secondary p-6 rounded-lg shadow-lg border border-gray-700 hover:border-accent transition-all duration-300 ease-in-out transform hover:-translate-y-1 animate-fade-in">
              <h3 className="text-xl font-semibold mb-2 text-accent">{arch.name}</h3>
              <p className="text-gray-300 mb-4">{arch.description}</p>
              <button
                className="mt-4 bg-accent text-primary font-bold py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors duration-200 ease-in-out"
                onClick={() => handleLoadArchitecture(arch.architecture_data)}
              >
                Load Architecture
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SavedArchitectures;
