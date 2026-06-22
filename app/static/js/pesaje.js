$(document).ready(function () {

    $('#fecha').on('change', function () {
        limpiarTodo();
        cargarVehiculos();
    });

    $('#vehiculo').on('change', function () {
        limpiarDesdeVehiculo();
        cargarClientes();
    });

    $('#cliente').on('change', function () {
        limpiarDesdeCliente();
        cargarManifiestos();
    });

    $('#recoleccion').on('change', function () {
        cargarDetalleManifiesto();
    });

    $('#btnGuardar').on('click', function (e) {
        e.preventDefault();
        guardarPesaje();
    });

});

$(document).ready(function () {
    $('#btnReporteAcumulados').on('click', function () {
        cargarReporteAcumulados();
    });
});

function limpiarTodo() {
    $('#vehiculo').html('<option value="">Seleccione...</option>');
    $('#cliente').html('<option value="">Seleccione...</option>');
    $('#recoleccion').html('<option value="">Seleccione...</option>');
    $('#tblDetalle tbody').html('');
}


function limpiarDesdeVehiculo() {
    $('#cliente').html('<option value="">Seleccione...</option>');
    $('#recoleccion').html('<option value="">Seleccione...</option>');
    $('#tblDetalle tbody').html('');
}


function limpiarDesdeCliente() {
    $('#recoleccion').html('<option value="">Seleccione...</option>');
    $('#tblDetalle tbody').html('');
}


function cargarVehiculos() {
    let fecha = $('#fecha').val();

    if (!fecha) {
        return;
    }

    fetch('/pesaje/vehiculos?fecha=' + fecha)
        .then(response => response.json())
        .then(data => {
            let html = '<option value="">Seleccione...</option>';

            data.forEach(v => {
                html += `<option value="${v.id}">${v.placa}</option>`;
            });

            $('#vehiculo').html(html);
        })
        .catch(error => {
            console.error('Error cargando vehículos:', error);
            alert('No se pudieron cargar las placas');
        });
}


function cargarClientes() {
    let fecha = $('#fecha').val();
    let vehiculo_id = $('#vehiculo').val();

    if (!fecha || !vehiculo_id) {
        return;
    }

    fetch(`/pesaje/clientes?fecha=${fecha}&vehiculo_id=${vehiculo_id}`)
        .then(response => response.json())
        .then(data => {
            let html = '<option value="">Seleccione...</option>';

            data.forEach(c => {
                html += `<option value="${c.id}">${c.razonSocial}</option>`;
            });

            $('#cliente').html(html);
        })
        .catch(error => {
            console.error('Error cargando clientes:', error);
            alert('No se pudieron cargar los clientes');
        });
}


function cargarManifiestos() {
    let fecha = $('#fecha').val();
    let vehiculo_id = $('#vehiculo').val();
    let cliente_id = $('#cliente').val();

    if (!fecha || !vehiculo_id || !cliente_id) {
        return;
    }

    fetch(`/pesaje/manifiestos?fecha=${fecha}&vehiculo_id=${vehiculo_id}&cliente_id=${cliente_id}`)
        .then(response => response.json())
        .then(data => {
            let html = '<option value="">Seleccione...</option>';

            data.forEach(r => {
                let texto = `Manifiesto #${r.id}`;

                if (r.hora) {
                    texto += ` - ${r.hora}`;
                }

                if (r.codigo_barras) {
                    texto += ` - ${r.codigo_barras}`;
                }

                html += `<option value="${r.id}">${texto}</option>`;
            });

            $('#recoleccion').html(html);
        })
        .catch(error => {
            console.error('Error cargando manifiestos:', error);
            alert('No se pudieron cargar los manifiestos');
        });
}


function cargarDetalleManifiesto() {
    let recoleccion_id = $('#recoleccion').val();

    if (!recoleccion_id) {
        $('#tblDetalle tbody').html('');
        return;
    }

    fetch('/pesaje/detalle-manifiesto/' + recoleccion_id)
        .then(response => response.json())
        .then(data => {
            let html = '';

            data.forEach(d => {
                html += `
                    <tr 
                        data-detalle-recoleccion-id="${d.id}"
                        data-tipo-residuo-id="${d.tipo_residuo_id}"
                    >
                        <td>${d.tipo_residuo}</td>

                        <td>
                            <input type="number"
                                   class="form-control bolsas"
                                   value="${d.bolsas || 0}"
                                   min="0">
                        </td>

                        <td>
                            <input type="number"
                                   class="form-control peso"
                                   value="${d.peso || 0}"
                                   step="0.01"
                                   min="0">
                        </td>

                        <td class="text-center">
                            <input type="checkbox"
                                   class="confirmado"
                                   checked>
                        </td>

                        <td>
                            <input type="text"
                                   class="form-control observaciones"
                                   value="${d.observaciones || ''}">
                        </td>
                    </tr>
                `;
            });

            $('#tblDetalle tbody').html(html);
        })
        .catch(error => {
            console.error('Error cargando detalle del manifiesto:', error);
            alert('No se pudo cargar el detalle del manifiesto');
        });
}

function guardarPesaje() {
    let fecha = $('#fecha').val();
    let vehiculo_id = $('#vehiculo').val();
    let cliente_id = $('#cliente').val();
    let recoleccion_id = $('#recoleccion').val();

    if (!fecha || !vehiculo_id || !cliente_id || !recoleccion_id) {
        alert('Debe seleccionar fecha, placa, cliente y manifiesto');
        return;
    }

    let detalles = [];

    $('#tblDetalle tbody tr').each(function () {
        detalles.push({
            detalle_recoleccion_id: parseInt($(this).data('detalle-recoleccion-id')),
            tipo_residuo_id: parseInt($(this).data('tipo-residuo-id')),
            bolsas: parseInt($(this).find('.bolsas').val() || 0),
            peso: parseFloat($(this).find('.peso').val() || 0),
            confirmado: $(this).find('.confirmado').is(':checked') ? 1 : 0,
            observaciones: $(this).find('.observaciones').val()
        });
    });

    if (detalles.length === 0) {
        alert('No hay residuos para guardar');
        return;
    }

    let payload = {
        recoleccion_id: parseInt(recoleccion_id),
        vehiculo_id: parseInt(vehiculo_id),
        cliente_id: parseInt(cliente_id),
        fecha: fecha,
        estado: 'CONFIRMADO',
        firma_verificacion: '',
        observaciones: '',
        detalles: detalles
    };

    fetch('/pesaje/guardar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error HTTP ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensaje || 'Pesaje guardado correctamente');
        window.location.reload();
    })
    .catch(error => {
        console.error('Error guardando pesaje:', error);
        alert('No se pudo guardar el pesaje');
    });
}

function cargarReporteAcumulados() {
    let fecha = $('#rep_fecha').val() || $('#fecha').val();

    if (!fecha) {
        alert('Seleccione una fecha para el reporte');
        return;
    }

    fetch(`/pesaje/reporte-acumulados?fecha=${fecha}`)
        .then(response => response.json())
        .then(data => {
            renderReporteAcumulados(data);
        })
        .catch(error => {
            console.error('Error cargando reporte:', error);
            alert('No se pudo cargar el reporte');
        });
}


function renderReporteAcumulados(data) {
    let html = `
        <div class="row">
            ${renderBloqueAcumulado('Día', data.dia)}
            ${renderBloqueAcumulado('Semana', data.semana)}
            ${renderBloqueAcumulado('Mes', data.mes)}
        </div>
    `;

    $('#reporteAcumulados').html(html);
}


function renderBloqueAcumulado(titulo, rows) {
    let total = 0;

    let filas = rows.map(r => {
        total += parseFloat(r.kg || 0);

        return `
            <tr>
                <td>${r.cliente}</td>
                <td class="text-right">${parseFloat(r.kg || 0).toFixed(2)}</td>
            </tr>
        `;
    }).join('');

    if (!filas) {
        filas = `
            <tr>
                <td colspan="2" class="text-center text-muted">Sin datos</td>
            </tr>
        `;
    }

    return `
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <strong>${titulo}</strong>
                </div>
                <div class="card-body p-0">
                    <table class="table table-sm table-striped mb-0">
                        <thead>
                            <tr>
                                <th>Cliente</th>
                                <th class="text-right">Kg</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${filas}
                        </tbody>
                        <tfoot>
                            <tr>
                                <th>Total</th>
                                <th class="text-right">${total.toFixed(2)}</th>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>
    `;
}

$(document).on('click', '#btnReporteAcumulados', function () {
    console.log('Click en Generar reporte');
    cargarReporteAcumulados();
});

$(document).on('click', '#btnImprimirReporte', function () {
    const contenido = document.getElementById('reporteAcumulados');

    if (!contenido || contenido.innerHTML.trim() === '') {
        alert('Primero genere el reporte.');
        return;
    }

    const ventana = window.open('', '_blank');

    ventana.document.write(`
        <html>
        <head>
            <title>Reporte de Pesaje y Clasificación</title>
            <link rel="stylesheet" href="/static/assets/bundles/lib.vendor.bundle.css">
            <link rel="stylesheet" href="/static/assets/css/main.css">
        </head>
        <body>
            <div class="container mt-4">
                <h3>Reporte de Pesaje y Clasificación</h3>
                <p>Fecha base: ${$('#rep_fecha').val() || $('#fecha').val()}</p>
                ${contenido.innerHTML}
            </div>
        </body>
        </html>
    `);

    ventana.document.close();
    ventana.focus();

    setTimeout(function () {
        ventana.print();
    }, 500);
});