import { env } from "@/config"

function buildUrlWithParams(
    url,
    params,
  ) {
    if (!params) return url;
    const filteredParams = Object.fromEntries(
      Object.entries(params).filter(
        ([, value]) => value !== undefined && value !== null,
      ),
    );
    if (Object.keys(filteredParams).length === 0) return url;
    const queryString = new URLSearchParams(
      filteredParams
    ).toString();
    return `${url}?${queryString}`;
  }
  
  async function fetchApi(
    url,
    options = {},
  ) {
    const {
      method = 'GET',
      headers = {},
      body,
      cookie,
      params,
      cache = 'no-store',
      next,
    } = options;
    const fullUrl = buildUrlWithParams(`${env.API_URL}${url}`, params);
  
    const response = await fetch(fullUrl, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...headers,
        ...(cookie ? { Cookie: cookie } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include',
      cache,
      next,
    });
  
    if (!response.ok) {
      const message = (await response.json()).message || response.statusText;
      if (typeof window !== 'undefined') {
        useNotifications.getState().addNotification({
          type: 'error',
          title: 'Error',
          message,
        });
      }
      throw new Error(message);
    }
  
    return response.json();
  }
  
  export const api = {
    get(url, options=null) {
      return fetchApi(url, { ...options, method: 'GET' });
    },
    post(url, body = null, options = null) {
      return fetchApi(url, { ...options , method: 'POST', body });
    },
    put(url, body = null, options = null) {
      return fetchApi(url, { ...options, method: 'PUT', body });
    },
    patch(url, body = null, options = null) {
      return fetchApi(url, { ...options, method: 'PATCH', body });
    },
    delete(url, options = null) {
      return fetchApi(url, { ...options, method: 'DELETE' });
    },
  };
  