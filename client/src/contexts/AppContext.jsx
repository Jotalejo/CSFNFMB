import { createContext, useCallback, useContext, useReducer } from 'react';
import {clientsService} from '@/services';

const initialState = {
  clientes: [],
  error: null,
  isLoading: false
}

const AppContext = createContext(initialState);

const AppDispatchContext = createContext(null);

export function AppProvider({ children }) {

  const [state, dispatch] = useReducer(
    appReducer,
    initialState
  );

  const loadClientes = useCallback(async ()=> {
    const data = await clientsService.getAll()
    console.log(data)
    dispatch({type: "clientes_loaded", 
      payload: {clientes: data, error: null}})
  })

  return (
    <AppContext.Provider value={state}>
      <AppDispatchContext.Provider value={{
          dispatch: dispatch,
          loadClientes: loadClientes
        }}
      >
        {children}
      </AppDispatchContext.Provider>
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}

export function useAppDispatch() {
  return useContext(AppDispatchContext);
}

function appReducer(state, action) {
  const {type, payload} = action;
  console.log("Reducer ", action.type, payload)
  switch (type) {
    case 'clientes_loaded': {
      const new_state = {...state, clientes: payload.clientes, error: payload.error, isLoading: false}
      console.log(new_state)
      return new_state
    }
    case 'cliente_deleted': {
      const new_clientes = state.clientes.filter(t => t.id !== payload.id)
      const new_state = {...state, clientes: new_clientes}
      return new_state
    }
    case 'added': {
      return [...clientes, {
        id: action.id,
        text: action.text,
        done: false
      }];
    }
    case 'changed': {
      return Clientes.map(t => {
        if (t.id === action.cliente.id) {
          return action.cliente;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return clientes.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}


