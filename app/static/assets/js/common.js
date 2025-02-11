function send_json(event) {
    event.preventDefault(); // Prevent the default form submission

    // Create an object to hold the form data
    const formData = {};
    const elements = event.target.elements;

    // Loop through the form elements and add them to the formData object
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        if (element.name) {
            formData[element.name] = element.value;
        }
    }

    // Convert the formData object to a JSON string
    const jsonRequest = JSON.stringify(formData);

    // Log the JSON request to the console (or send it to a server)
    console.log(jsonRequest);
    
    const method = formData.id && formData.id > 0? "PATCH": "POST";

    // Example of sending the JSON request to a server using fetch
    fetch(event.target.action, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonRequest
    })
    .then(response => response.json())
    .then(data => console.log('Success:', data))
    .catch(error => console.error('Error:', error));
};