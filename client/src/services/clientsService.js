import { api } from "./api";


export const clientsService = {
    getAll() {
        return api.get('/clientes');
    },


}