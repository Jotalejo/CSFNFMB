function send_json(event) {
    event.preventDefault(); // Prevent the default form submission

    // Create an object to hold the form data
    const formData = {};
    const form = event.target;
    const elements = form.elements;

    // Loop through the form elements and add them to the formData object
    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        if (element.name && 
            element.type !== 'button' && 
            element.type !== 'submit' && 
            !element.closest('table.data-array')) {
            // Solo procesamos elementos que NO están dentro de una tabla con clase table-array
            formData[element.name] = element.value;
        }
    }

    // Procesar tablas con clase table-array
    const tablesArray = form.querySelectorAll('table.data-array');
    tablesArray.forEach(table => {
        const tableId = table.id || 'table_data';
        const rows = table.querySelectorAll('tbody tr');
        const tableData = [];

        rows.forEach(row => {
            const rowData = {};
            const inputs = row.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                if (input.name) {
                    // Remover [] del nombre si existe
                    const fieldName = input.name.replace(/\[\]$/, '');
                    rowData[fieldName] = input.value;
                }
            });

            // Solo agregar la fila si tiene datos
            if (Object.keys(rowData).length > 0) {
                tableData.push(rowData);
            }
        });

        formData[tableId] = tableData;
    });    

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
    .then(data => {
            let redirectPage = event.target.getAttribute('data-redirect');
            console.log('Success:', redirectPage)
            if (redirectPage) {
                window.location.href = redirectPage;
            }
        }
    )
    .catch(error => console.error('Error:', error));
};

function send_form(frmId) {
    const form = document.getElementById(frmId);

    const formData = {};
    const elements = Array.from(form.querySelectorAll('input, select, textarea'));

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
    fetch(form.action, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonRequest
    })
    .then(response => response.json())
    .then(data => {
            let redirectPage = event.target.getAttribute('data-redirect');
            console.log('Success:', redirectPage)
            if (redirectPage) {
                window.location.href = redirectPage;
            }
        }
    )
    .catch(error => console.error('Error:', error));

}
