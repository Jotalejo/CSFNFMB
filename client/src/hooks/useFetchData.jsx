import { useState, useEffect } from 'react';


export const useFetchData = (get_data) =>
{
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async() => {

    
    console.log('Getting data')
    setLoading(true);
    try {
      const data = await get_data()
      setData(data)
    }
    catch (error) {
        setError(error)
        console.log(error)
    }
    finally {
        setLoading(false)
    }
  }
  fetchData()
  }, []);

  return { data, error, loading };
}
