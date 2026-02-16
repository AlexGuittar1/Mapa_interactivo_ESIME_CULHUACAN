import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import MapPage from './pages/MapPage';
import Dashboard from './pages/Dashboard';
import ParkingPage from './pages/ParkingPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/parking" element={<ParkingPage />} />
      </Routes>
    </Router>
  );
}

export default App;
