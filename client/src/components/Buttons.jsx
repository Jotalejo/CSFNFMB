import Button from '@mui/material/Button';

const withDefaultProps = (Component, defaultProps) => {
    return (props) => <Component {...defaultProps} {...props}></Component>
}


export const EditButton = ({text="Editar", onClick}) => {
    return <Button variant="contained" onClick={onClick}>{text}</Button>
}

export const DeleteButton = ({text="Eliminar", onClick}) => {
    return <Button variant="contained" onClick={onClick}>{text}</Button>
}