
import { DataGrid } from "@mui/x-data-grid";
/*import {
  DeleteButton,
  EditButton,
  List,
  ShowButton,
  useDataGrid,
} from "@refinedev/mui";
 */

import React, { Suspense, useEffect } from "react";
import Page from '../../components/Page';
import { EditButton, DeleteButton } from "@/components"
import { useApp, useAppDispatch } from "../../contexts/AppContext";
import { useNavigate } from "react-router";
import { Loading } from "../../components/Loading";
import { clientsService } from "../../services/clientsService";
import { useClientsStore } from "../../contexts/clients";
import { useLoaderData } from 'react-router';
import { redirect } from "react-router";

const Content = (clientes) => {

  return <DataGrid rows={clientes}  columns={columns} />
}


export const ClientList = () => {
  const clients = useLoaderData();
  const {actions, dispatch} = useAppDispatch()
  const navigate = useNavigate()

  console.log(clients);
  

  const handleEdit = (id) => {
    console.log('handle edit', id)
    navigate(`/clientes/${id}`)
  }

  const handleDelete = (id) => {
    dispatch({type: "cliente_deleted", payload: {id}})
    console.log(id)
  }

  const columns = React.useMemo(
    () => [
      {
        field: "nit",
        headerName: "NIT",
        type: "string",
        minWidth: 50,
      },
      {
        field: "razonSocial",
        flex: 1,
        headerName: "Razon Social",
        minWidth: 200,
      },
      {
        field: "actions",
        headerName: "Acciones",
        sortable: false,
        renderCell: function render({ row }) {
          return (
            <>
              <EditButton hideText recordItemId={row.id} onClick={()=>{ handleEdit(row.id)}}/>
              <DeleteButton hideText recordItemId={row.id} onClick={()=>{ handleDelete(row.id)}} />
            </>
          );
        },
        align: "center",
        headerAlign: "center",
        minWidth: 80,
      },
    ],
    []
  );


  return (
    <Page title="Clientes">
      <Suspense fallback={<Loading />}>
        <DataGrid rows={clients}  columns={columns} />
      </Suspense>
    </Page>
  );
};
