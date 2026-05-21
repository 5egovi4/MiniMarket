const API = 'http://127.0.0.1:8000/api/productos'
let productoAEliminar = null

// Navegación 
function mostrarSeccion(nombre) {
    document.querySelectorAll('.dashboard-section').forEach(s => s.style.display = 'none')
    document.querySelectorAll('.sidebar-btn').forEach(b => b.classList.remove('active'))
    document.getElementById(`seccion-${nombre}`).style.display = 'block'
    event.currentTarget.classList.add('active')
    if (nombre === 'inventario') cargarProductos()
    if (nombre === 'agregar') limpiarForm()
}

// Cargar inventario 
async function cargarProductos() {
    const res = await fetch(`${API}/listar/`)
    const productos = await res.json()
    const grid = document.getElementById('lista-productos')
    const total = document.getElementById('total-productos')
    total.textContent = `${productos.length} producto${productos.length !== 1 ? 's' : ''}`
    if (productos.length === 0) {
        grid.innerHTML = `<div class="empty-state">
            <span>📭</span>
            <p>No hay productos en el inventario</p>
        </div>`
        return
    }
    grid.innerHTML = productos.map(p => `
        <div class="prod-card">
            <div class="prod-img-wrap">
                ${p.foto
                    ? `<img src="${p.foto}" alt="${p.nombre}" onerror="this.style.display='none'">`
                    : `<span class="prod-no-img">🛒</span>`
                }
            </div>
            <div class="prod-info">
                <h3>${p.nombre}</h3>
                <div class="prod-meta">
                    <span class="prod-precio">$${parseFloat(p.precio).toLocaleString('es-CO')}</span>
                    <span class="prod-stock">Stock: ${p.stock}</span>
                </div>
            </div>
            <div class="prod-acciones">
                <button class="btn-editar-prod" onclick="editarProducto(${JSON.stringify(p).replace(/"/g, '&quot;')})">✏️</button>
                <button class="btn-eliminar-prod" onclick="pedirEliminar(${p.id_producto}, '${p.nombre}')">🗑️</button>
            </div>
        </div>
    `).join('')
}

//  Guardar (crear o actualizar) 
async function guardarProducto() {
    const id = document.getElementById('producto-id').value
    const nombre = document.getElementById('prod-nombre').value
    const precio = document.getElementById('prod-precio').value
    const stock = document.getElementById('prod-stock').value
    const foto = document.getElementById('prod-foto').files[0]  

    if (!nombre || !precio || !stock) {
        alert('Nombre, precio y stock son obligatorios')
        return
    }

    const formData = new FormData()
    formData.append('nombre', nombre)
    formData.append('precio', precio)
    formData.append('stock', stock)
    if (foto) formData.append('foto', foto)

    const url = id ? `${API}/${id}/actualizar/` : `${API}/agregar/`
    const method = id ? 'PUT' : 'POST'

    const res = await fetch(url, {
        method,
        body: formData  
    })

    if (res.ok) {
        alert(id ? 'Producto actualizado' : 'Producto creado')
        mostrarSeccionDirecta('inventario')
    } else {
        alert('Error al guardar el producto')
    }
}

//  Editar 
function editarProducto(p) {
    document.getElementById('producto-id').value = p.id_producto
    document.getElementById('prod-nombre').value = p.nombre
    document.getElementById('prod-precio').value = p.precio
    document.getElementById('prod-stock').value = p.stock
    document.getElementById('prod-foto').value = p.foto || ''
    document.getElementById('form-titulo').textContent = 'Editar producto'
    if (p.foto) {
        document.getElementById('preview-img').src = p.foto
        document.getElementById('foto-preview').style.display = 'block'
    }
    mostrarSeccionDirecta('agregar')
}
//  Eliminar 
function pedirEliminar(id, nombre) {
    productoAEliminar = id
    document.getElementById('modal-nombre-producto').textContent = nombre
    document.getElementById('modal-eliminar').style.display = 'flex'
}
async function confirmarEliminar() {
    const res = await fetch(`${API}/${productoAEliminar}/eliminar/`, { method: 'DELETE' })
    cerrarModal()
    if (res.ok) {
        cargarProductos()
    } else {
        alert('Error al eliminar')
    }
}
function cerrarModal() {
    document.getElementById('modal-eliminar').style.display = 'none'
    productoAEliminar = null
}

    //  Helpers 
function limpiarForm() {
    document.getElementById('producto-id').value = ''
    document.getElementById('prod-nombre').value = ''
    document.getElementById('prod-precio').value = ''
    document.getElementById('prod-stock').value = ''
    document.getElementById('prod-foto').value = ''
    document.getElementById('foto-preview').style.display = 'none'
    document.getElementById('form-titulo').textContent = 'Agregar producto'
}
function cancelarForm() {
    mostrarSeccionDirecta('inventario')
}
function mostrarSeccionDirecta(nombre) {
    document.querySelectorAll('.dashboard-section').forEach(s => s.style.display = 'none')
    document.querySelectorAll('.sidebar-btn').forEach(b => b.classList.remove('active'))
    document.getElementById(`seccion-${nombre}`).style.display = 'block'
}

// Preview de foto en tiempo real
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('prod-foto').addEventListener('input', function() {
        const preview = document.getElementById('foto-preview')
        const img = document.getElementById('preview-img')
        if (this.value) {
            img.src = this.value
            preview.style.display = 'block'
        } else {
            preview.style.display = 'none'
        }
    })
    cargarProductos()
})

function cerrarSesion() {
    localStorage.removeItem('usuarioId')
    localStorage.removeItem('rol')
    window.location.href = '/FrontEnd/login.html'
}