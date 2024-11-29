import { api } from "./api";


export const clientsService = {
    getAll: () => {
        return api.get('/clientes');
    },
    getById : (id) => {
        return api.get(`/clientes/${id}`)
    },
    update : (cliente) => {
        return api.patch(`/clientes/${cliente,id}`, cliente)
    },
    create : async (cliente) => {
        return api.post(`/clientes`, cliente)
    }
}