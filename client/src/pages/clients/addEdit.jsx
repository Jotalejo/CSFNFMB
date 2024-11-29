import Page from '@/components/Page';
import { TextField, Box, Button } from '@mui/material';
import { useLoaderData } from 'react-router';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { api } from '@/services/api'
import { useNavigate } from "react-router";

export const AddEditClient = () => {

    const client = useLoaderData()
    const navigate = useNavigate()

    const { register, handleSubmit, errors, control } = useForm({defaultValues: client});
    const id = Number(client?.id)
    const isAddMode = !id
    const onSubmit = async (data) => {
        if (isAddMode) {
            await api.post("/clientes", data);
        }
        else {
            await api.patch(`/clientes/${id}`, data);
        }

        navigate('/clientes')
    }

    console.log(id, isAddMode)

    return (
        <Page title="Cliente">
            <Box
                component="form"
                sx={{ display: "flex", flexDirection: "column" }}
                autoComplete="off"
                onSubmit={handleSubmit(onSubmit)}
            >
                <TextField name="nit" label="NIT" error={errors?.nit}
                    {...register('nit', { required: true })}
                    variant="standard" 
                    /> 
                <TextField name="razonSocial" label="Razon Social" error={errors?.razonSocial}
                    {...register('razonSocial', { required: true })}
                    variant="standard" 
                    />            
                <TextField name="direccion" label="Dirección" error={errors?.direccion}
                    {...register('direccion', { required: false })}
                    variant="standard" 
                    />
                <TextField name="telefono" label="Telefono" error={errors?.telefono}
                    {...register('telefono', { required: false })}
                    variant="standard" 
                    />
                <TextField name="ciudad" label="Ciudad" error={errors?.ciudad}
                    {...register('ciudad', { required: false })}
                    variant="standard" 
                    />
                <TextField name="actividad" label="Actividad" error={errors?.actividad}
                    {...register('actividad', { required: false })}
                    variant="standard" 
                    />    
                <TextField name="contacto" label="Contacto" error={errors?.contacto}
                    {...register('contacto', { required: false })}
                    variant="standard" 
                    />  
                <TextField name="telefonoContacto" label="Telefono contacto" error={errors?.telefonoContacto}
                    {...register('telefonoContacto', { required: false })}
                    variant="standard" 
                    /> 
                <TextField name="observaciones" label="Observaciones" error={errors?.observaciones}
                    fullWidth multiline maxRows={4}
                    {...register('observaciones', { required: false })}
                    variant="standard" 
                    />  
               
                <Button type="submit">Guardar</Button>
            </Box>            

        </Page>
    )
}