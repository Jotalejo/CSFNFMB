import * as React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import Dashboard from './dashboard/Dashboard';
import { BrowserRouter, Outlet, Route, Routes, Navigate  } from "react-router-dom";
import { ClientList } from './pages/clients/lists';
import { AppProvider } from './contexts/AppContext';

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Dashboard />}>
            <Route index element={<></>}></Route>
            <Route path="clientes" element={<ClientList />}></Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}


/**
 *     <Container maxWidth="sm">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" sx={{ mb: 2 }}>
          Material UI Vite.js example
        </Typography>
        <ProTip />
        <Copyright />
      </Box>
    </Container>

 * 
 */