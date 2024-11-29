import { createContext, useCallback, useContext } from 'react';
import {clientsService} from '@/services';
import useAsyncReducer from '@/hooks/useAsyncReducer';

const initialState = {
  clientes: [],
  error: null,
  isLoading: false
}

const createActions = (dispatch) => {
  return {
    loadClientes: () => dispatch({type: "load_clientes"}),
    createCliente: (cliente) => dispatch({type: "add_cliente"})
  }
}

function appReducer(state, action) {
  const {type, payload} = action
  return new Promise(resolve=>{
    switch (type) {
      case "load_clientes":
        clientsService.getAll().then(data => resolve({...state, clientes: data}))
      case "add_cliente":
        clientsService.update(cliente).then(data => {
          
        })
    }
  })
}


const AppContext = createContext(initialState);

const AppDispatchContext = createContext(null);

export function AppProvider({ children }) {

  const [state, dispatch] = useAsyncReducer(
    appReducer,
    initialState
  );

  const actions = createActions(dispatch)

  return (
    <AppContext.Provider value={state}>
      <AppDispatchContext.Provider value={{
          dispatch: dispatch,
          actions: actions,
          //loadClientes: loadClientes
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


/*
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
    case 'cliente_added': {
      
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
*/

