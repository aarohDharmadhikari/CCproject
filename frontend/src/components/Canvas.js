import React, { useState, useCallback, useEffect, useRef } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import Dashboard from './Dashboard';

let id = 0;
const getId = () => `dndnode_${id++}`;

// Debounce function
const debounce = (func, delay) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, delay);
  };
};

const Canvas = ({ selectedLab, setSelectedLab, architectureToLoad, setArchitectureToLoad }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [components, setComponents] = useState([]);
  const [simulationResult, setSimulationResult] = useState(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [labStatus, setLabStatus] = useState(null);
  const [loading, setLoading] = useState(false); // New loading state

  // Effect to fetch components from backend
  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/components');
        setComponents(response.data);
      } catch (error) {
        console.error("Failed to fetch components", error);
      }
    };
    fetchComponents();
  }, []);

  // Effect to load architecture when architectureToLoad changes
  useEffect(() => {
    if (architectureToLoad) {
      setNodes(architectureToLoad.nodes);
      setEdges(architectureToLoad.edges);
      // Reset ID counter to avoid conflicts with loaded nodes
      id = architectureToLoad.nodes.length > 0 
           ? Math.max(...architectureToLoad.nodes.map(node => parseInt(node.id.replace('dndnode_', '') || 0))) + 1
           : 0;
      setArchitectureToLoad(null); // Clear after loading
      setSelectedLab(null); // Clear any active lab when loading a saved architecture
      setLabStatus(null);
      setSimulationResult(null);
    }
  }, [architectureToLoad, setArchitectureToLoad, setSelectedLab]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );

  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const reactFlowBounds = reactFlowInstance.project({ x: event.clientX, y: event.clientY });
      const type = event.dataTransfer.getData('application/reactflow');
      const component = components.find(c => c.type === type);

      if (typeof type === 'undefined' || !type || !component) {
        return;
      }

      const newNode = {
        id: getId(),
        type: 'default',
        position: { x: reactFlowBounds.x, y: reactFlowBounds.y },
        data: { label: `${component.name}`, componentType: component.type },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, components]
  );
  
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const performSimulation = async () => {
    setLoading(true); // Start loading
    const architecture = { 
      nodes: nodes.map(n => ({ id: n.id, type: n.data.componentType || n.type })),
      edges: edges.map(e => ({ id: e.id, source: e.source, target: e.target }))
    };
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/simulate', architecture);
      setSimulationResult(response.data);

      if (selectedLab) {
        if (response.data.estimated_cost_usd <= selectedLab.target_cost) {
          setLabStatus('completed');
        } else {
          setLabStatus('in-progress');
        }
      }
    } catch (error) {
      console.error("Failed to run simulation", error);
    } finally {
      setLoading(false); // End loading
    }
  };

  // Debounced version of the simulation function
  const debouncedSimulate = useCallback(debounce(performSimulation, 500), [nodes, edges, selectedLab]);

  // Trigger debounced simulation when nodes or edges change
  useEffect(() => {
    debouncedSimulate();
  }, [nodes, edges, debouncedSimulate]);


  const resetCanvas = () => {
    setNodes([]);
    setEdges([]);
    setSimulationResult(null);
    setLabStatus(null);
    setSelectedLab(null); // Also clear selected lab when resetting canvas
    id = 0; // Reset ID counter
  };

  return (
    <div className="flex h-full">
      <div className="w-1/4 p-4 border-r border-secondary">
        {selectedLab ? (
          <div className="mb-4 p-4 bg-secondary rounded-lg border border-accent">
            <h3 className="text-xl font-bold mb-2 text-accent">{selectedLab.title}</h3>
            <p className="text-gray-300 mb-2">{selectedLab.description}</p>
            <p className="text-sm text-gray-400 mb-4">Target Cost: ${selectedLab.target_cost}</p>
            {labStatus === 'completed' && <p className="text-green-500 font-bold">Lab Completed!</p>}
            {labStatus === 'in-progress' && <p className="text-yellow-500 font-bold">Lab In Progress...</p>}
            <button onClick={resetCanvas} className="w-full mt-2 bg-red-500 text-white font-bold py-2 px-4 rounded hover:bg-red-600 transition-colors">
              Exit Lab
            </button>
          </div>
        ) : (
          <h3 className="text-xl font-bold mb-4">Components</h3>
        )}
        
        <div className="mt-4">
          {components.map((component) => (
            <div
              key={component.type}
              className="p-2 mb-2 border border-accent rounded cursor-pointer"
              onDragStart={(event) => onDragStart(event, component.type)}
              draggable
            >
              {component.name}
            </div>
          ))}
        </div>

        <button onClick={performSimulation} className="w-full mt-4 bg-accent text-primary font-bold py-2 px-4 rounded hover:bg-blue-600 transition-colors" disabled={loading}>
          {loading ? (
            <div className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Simulating...
            </div>
          ) : (
            'Simulate'
          )}
        </button>
        <button onClick={resetCanvas} className="w-full mt-2 bg-gray-600 text-white font-bold py-2 px-4 rounded hover:bg-gray-700 transition-colors">
          Clear Canvas
        </button>
        {simulationResult && <Dashboard data={simulationResult} />}
      </div>
      <div className="w-3/4" style={{ height: '90vh' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onInit={setReactFlowInstance}
          onDrop={onDrop}
          onDragOver={onDragOver}
          fitView
        >
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
    </div>
  );
};

export default Canvas;
