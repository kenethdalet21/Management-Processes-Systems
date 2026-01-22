import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { useAuth } from './context/AuthContext';

// Layout
import Layout from './components/Layout/Layout';

// Components (OfflineDetector temporarily disabled for development)
// import OfflineDetector from './components/OfflineDetector';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ProductManagement from './pages/ProductManagement';
import InventoryManagement from './pages/InventoryManagement';
import SalesManagement from './pages/SalesManagement';
import PayrollManagement from './pages/PayrollManagement';
import FinancialManagement from './pages/FinancialManagement';
import Settings from './pages/Settings';
import TabPermissions from './pages/TabPermissions';

function App() {
  const { user } = useAuth();

  return (
    <>
      {/* <OfflineDetector /> */}
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
          
          <Route element={user ? <Layout /> : <Navigate to="/login" />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<ProductManagement />} />
            <Route path="/inventory" element={<InventoryManagement />} />
            <Route path="/sales" element={<SalesManagement />} />
            <Route path="/payroll" element={<PayrollManagement />} />
            <Route path="/financial" element={<FinancialManagement />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/tab-permissions" element={<TabPermissions />} />
          </Route>
        </Routes>
      </Box>
    </>
  );
}

export default App;
