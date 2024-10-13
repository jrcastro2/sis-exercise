import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SearchPage from './components/SearchPage';
import StatsPage from './components/StatsPage';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div className="base-app">
      <Routes>
          <Route path="/search" element={<SearchPage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/" element={<Navigate to="/search" replace />} />
          </Routes>
      </div>
    </Router>
  );
};

export default App;