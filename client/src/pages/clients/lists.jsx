
import { DataGrid } from "@mui/x-data-grid";
/*import {
  DeleteButton,
  EditButton,
  List,
  ShowButton,
  useDataGrid,
} from "@refinedev/mui";
 */

import React, { useEffect } from "react";
import Page from '../../components/Page';
import { EditButton, DeleteButton } from "@/components"
import { useApp, useAppDispatch } from "../../contexts/AppContext";


export const ClientList = () => {
  const {clientes} = useApp()
  const {loadClientes, dispatch} = useAppDispatch()

  const handleEdit = (id) => {
    console.log(id)
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
        headerName: "Actions",
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

  useEffect(()=> {
    loadClientes();
  }, [])

  return (
    <Page title="Clientes">
      <DataGrid rows={clientes}  columns={columns} />
    </Page>
  );
};
