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