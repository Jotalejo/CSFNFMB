import React from 'react';
import Dashboard from '../../dashboard/Dashboard';

const Layout = ({ children }) => {
  return (
    <Dashboard>
        {children}
    </Dashboard>
  );
}

export default Layout;