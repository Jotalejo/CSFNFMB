export const wrapPromise = (promise) => {
    let status = 'pending'
    let response

    const suspender = promise.then((result)=> {
        status = 'success'
        response = result
    },
    (error) => {
        status = 'error'
        response = error
    })

    const read = () => {
        switch (status) {
            case 'pending':
                throw suspender
            case 'error':
                throw response
            default:
                return response
        }
    }

    return {read}
}