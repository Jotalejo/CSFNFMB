
const createEnv = () => {
    const envVars = {
        API_URL: process.env.API_URL,
    }

    return envVars;
}

export const env = createEnv();

