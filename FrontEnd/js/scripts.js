const imagenes = [
  "./img/publicidad1.jpg",
  "./img/publicidad2.jpg",
];

let indiceActual = 0;

const img = document.getElementById("carrusel");

function mostrarImagen() {
  img.src = imagenes[indiceActual];
}

function siguiente() {
  indiceActual++;

  if (indiceActual >= imagenes.length) {
    indiceActual = 0; 
  }

  mostrarImagen();
}

function anterior() {
  indiceActual--;

  if (indiceActual < 0) {
    indiceActual = imagenes.length - 1; 
  }

  mostrarImagen();
}

async function registrarUsuario() {
    const nombre = document.getElementById('nombre').value
    const apellido = document.getElementById('apellido').value
    const email = document.getElementById('correo').value
    const contraseña = document.getElementById('contraseña').value
    const confirmar = document.getElementById('confirmar-contraseña').value

    if (contraseña !== confirmar) {
        alert('Las contraseñas no coinciden')
        return
    }

    const response = await fetch(`http://127.0.0.1:8000/api/usuarios/registrar/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: nombre,
            apellido: apellido,
            email: email,
            contraseña: contraseña,
            rol: 'cliente'
        })
    })

    const data = await response.json()

    if (response.ok) {
        alert('Cuenta creada exitosamente')
        window.location.href = 'login.html'
    } else {
        alert('Error: ' + JSON.stringify(data))
    }
}

async function iniciarSesion() {
    const email = document.getElementById('userId').value
    const contraseña = document.getElementById('password').value

    const response = await fetch(`http://127.0.0.1:8000/api/usuarios/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          contraseña: contraseña
        })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('usuarioId', data.usuario.id_usuario)
    alert('Bienvenido ' + data.usuario.nombre)
        if (data.usuario.rol === 'admin') {
            window.location.href = 'dashboard.html'
        } else {
                window.location.href = 'home.html'
        }    
    } else {
    alert('Credenciales incorrectas')
    }
}

const usuarioId = localStorage.getItem('usuarioId') || 1

async function cargarPerfil() {
    const response = await fetch(`http://127.0.0.1:8000/api/usuarios/${usuarioId}/`)
    const usuario = await response.json()

    document.getElementById('display-nombre').textContent = `${usuario.nombre} ${usuario.apellido}`
    document.getElementById('display-rol').textContent = usuario.rol
    document.getElementById('display-email').textContent = usuario.email
    document.getElementById('display-telefono').textContent = usuario.num_telefono || '—'
    document.getElementById('display-direccion').textContent = usuario.direccion || '—'
    document.getElementById('display-fecha').textContent = usuario.fecha_registro

    document.getElementById('edit-nombre').value = usuario.nombre
    document.getElementById('edit-apellido').value = usuario.apellido
    document.getElementById('edit-telefono').value = usuario.num_telefono || ''
    document.getElementById('edit-direccion').value = usuario.direccion || ''
}

function mostrarFormulario() {
    document.getElementById('vista-info').style.display = 'none'
    document.getElementById('vista-formulario').style.display = 'block'
}

function cancelarEdicion() {
    document.getElementById('vista-formulario').style.display = 'none'
    document.getElementById('vista-info').style.display = 'block'
}

async function guardarCambios() {
    const response = await fetch(`http://127.0.0.1:8000/api/usuarios/${usuarioId}/actualizar/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: document.getElementById('edit-nombre').value,
            apellido: document.getElementById('edit-apellido').value,
            num_telefono: document.getElementById('edit-telefono').value,
            direccion: document.getElementById('edit-direccion').value,
        })
    })

    if (response.ok) {
        alert('Perfil actualizado correctamente')
        cancelarEdicion()
        cargarPerfil()
    } else {
        alert('Error al actualizar el perfil')
    }
}

async function eliminarCuenta() {
    const confirmar = confirm('¿Estás seguro que deseas eliminar tu cuenta? Esta acción no se puede deshacer.')
    if (!confirmar) return

    const response = await fetch(`http://127.0.0.1:8000/api/usuarios/${usuarioId}/eliminar/`, {
        method: 'DELETE'
    })

    if (response.ok) {
        alert('Cuenta eliminada correctamente')
        window.location.href = 'login.html'
    } else {
        alert('Error al eliminar la cuenta')
    }
}

cargarPerfil()

function abrirCarrito() {
    document.getElementById('cart-drawer').classList.add('active')
    document.getElementById('cart-overlay').classList.add('active')
    document.body.style.overflow = 'hidden'
    cargarProductosCarrito()
}

function cerrarCarrito() {
    document.getElementById('cart-drawer').classList.remove('active')
    document.getElementById('cart-overlay').classList.remove('active')
    document.body.style.overflow = ''
}

async function agregarAlCarrito(id_producto) {
    
    const response = await fetch(`http://127.0.0.1:8000/api/carrito/agregar_producto/`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            id_usuario: localStorage.getItem('usuarioId'), 
            id_producto_id: id_producto,
            cantidad: 1 
        })}
    )
    
    const producto = await response.json()
    console.log(producto)
    if (response.ok) {
        alert('Producto agregado al carrito') 
    } else {
        alert("Error al agregar el producto")
    }
}


async function cargarProductosHome() {
    const res = await fetch('http://127.0.0.1:8000/api/productos/listar/')
    const productos = await res.json()

    const grid = document.querySelector('.products-grid')
    if (!grid) return

    if (productos.length === 0) {
        grid.innerHTML = '<p style="padding:1rem">No hay productos disponibles</p>'
        return
    }

    grid.innerHTML = productos.map(p => `
        <div class="product-card">
            <div class="product-image">
                ${p.foto
                    ? `<img src="http://127.0.0.1:8000${p.foto}" class="product-placeholder">`
                    : `<span style="font-size:3rem">🛒</span>`
                }
            </div>
            <div class="product-info">
                <div class="product-price">$${parseFloat(p.precio).toLocaleString('es-CO')}</div>
                <div class="product-name">${p.nombre}</div>
            </div>
            <button class="add-button" onclick="agregarAlCarrito(${p.id_producto})">Agregar</button>
        </div>
    `).join('')
}

cargarProductosHome()

async function cargarProductosCarrito() {
    const res = await fetch(`http://127.0.0.1:8000/api/carrito/${usuarioId}/ver_carrito/`)
    const productos = await res.json()

    const grid = document.querySelector('.cart-drawer-items')

    if (productos.length === 0) {
        grid.innerHTML = `
        <div class="cart-empty"> 
            <span>🛒</span> 
            <p>Tu carrito está vacío</p> 
        </div>`
        return
    }

    grid.innerHTML = productos.map( p => `
        <div class="cart-drawer-item">
            <img src="${`http://127.0.0.1:8000${p.id_producto.foto}`}">
            <div class="cart-item-info">
                <div class="item-title">${p.id_producto.nombre}</div>
                <div class="item-price">${p.id_producto.precio}</div>
            </div>
            <div class="item-price">Cantidad: ${p.cantidad}</div>
        </div>
        
        `).join('')
    await obtenerTotal()
}

async function obtenerTotal() {
    const usuarioId = localStorage.getItem('usuarioId')
    const res = await fetch(`http://127.0.0.1:8000/api/carrito/${usuarioId}/total/`)
    const data = await res.json()
    if (res.ok) {
        document.getElementById('cart-total').textContent = `$${parseFloat(data.total).toLocaleString('es-CO')}`
    }
}