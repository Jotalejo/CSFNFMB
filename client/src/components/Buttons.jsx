import Button from '@mui/material/Button';


export const EditButton = ({text="Editar"}) => {
    return <Button variant="contained">{text}</Button>
}

export const DeleteButton = ({text="Eliminar", onClick}) => {
    return <Button variant="contained" onClick={onClick}>{text}</Button>
}