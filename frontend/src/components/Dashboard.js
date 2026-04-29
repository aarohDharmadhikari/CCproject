import React from 'react';

const Dashboard = ({ data }) => {
  if (!data) {
    return null;
  }

  const hasWarning = data.message && data.message.toLowerCase().includes('warning');

  return (
    <div className="mt-4 p-4 bg-secondary rounded-lg shadow-lg border border-gray-700 animate-fade-in">
      <h3 className="text-xl font-bold mb-3 text-accent">Simulation Results</h3>
      <div className="space-y-2">
        <p className="text-gray-300">
          Estimated Cost: <span className="font-semibold text-white">${data.estimated_cost_usd.toFixed(2)}</span>
        </p>
        <p className="text-gray-300">
          Performance Score: <span className="font-semibold text-white">{data.performance_score}</span>
        </p>
      </div>
      <p className={`text-sm mt-3 ${hasWarning ? 'text-yellow-500' : 'text-gray-400'}`}>
        {data.message}
      </p>
    </div>
  );
};

// Add this to your tailwind.config.js if you want a custom animation
// theme: {
//   extend: {
//     animation: {
//       'fade-in': 'fadeIn 0.5s ease-out',
//     },
//     keyframes: {
//       fadeIn: {
//         '0%': { opacity: '0' },
//         '100%': { opacity: '1' },
//       },
//     },
//   },
// },

export default Dashboard;
