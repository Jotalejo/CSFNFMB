import { create } from 'zustand'
import { api } from "@/services/api";

export const useClientsStore = create((set) => ({
    clients: [],
    getAll: async () => {
      const response = await api.get('clientes')
      set({ clients: await response.json() })
    },
  }))

