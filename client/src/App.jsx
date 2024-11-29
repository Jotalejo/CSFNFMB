import * as React from 'react';
import Dashboard from './dashboard/Dashboard';
import { Route, 
  createBrowserRouter,
  createRoutesFromElements, 
  RouterProvider } from "react-router";
import { ClientList, AddEditClient } from './pages/clients';
import { AppProvider } from './contexts/AppContext';
import { clientsService } from './services/clientsService';
import { api } from './services/api';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route element={<Dashboard />}>
      <Route index element={<></>}></Route>
      <Route path="clientes" 
        loader={async ()=>{ return api.get('/clientes') }}
        element={<ClientList />}>
      </Route>
      <Route path='clientes/:id'
            loader={async ({params})=>{ 
                const client = await api.get(`/clientes/${params.id}`)
                console.log(client)
                return client
              }
            }
            element={<AddEditClient />}
          >
      </Route>
    </Route>
  ),
  {
  }
)

export default function App() {
  return (
    <AppProvider>
      <RouterProvider router={router}>
      </RouterProvider>
    </AppProvider>
  );
}
