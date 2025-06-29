import { useState } from 'react'
import './App.css'
import Home from './layouts/Home'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Nav from './components/Nav';
import PetsContainer from './components/PetsContainer';
import Carrito from './components/Carrito';
import About from './components/About';
import Contacto from './components/Contacto';
import PetDetalle from './components/PetDetalle';
import Admin from './components/Admin';
import Login from './components/Login';
import CarritoContainer from './components/CarritoContainer';
import AdopcionForm from './components/AdopcionForm';


function App() {
  const [petsCarrito, setPetsCarrito] = useState([] )
  const [usuarioLogeado, setUsuarioLogeado] = useState(false)
  const [adminLogeado, setAdminLogeado] = useState(false)

  function funcionCarrito(pet){
    const existe = petsCarrito.find(p => p.id === pet.id); //p=pet, (no va pet xq ya está expresado para otra cosa) podría ser p
    console.log(existe)
    if (existe) {
        const carritoActualizado = petsCarrito.map((p) => {
            if (p.id === pet.id){
                const petActualizado = {...p, cantidad: p.cantidad + pet.cantidad}
                return petActualizado
            }else{
                return p
            }
        })
        setPetsCarrito(carritoActualizado)
    }else{
        // Si no existe, lo agregamos con su cantidad
        const nuevoCarrito = [...petsCarrito, pet];
        setPetsCarrito(nuevoCarrito)
    }

 
  }


  function borrarPetCarrito(id){
    console.log(id)
    const nuevoCarrito = petsCarrito.filter((p) => p.id !== id);
    setPetsCarrito(nuevoCarrito);
  }

  function manejarAdmin() {
    setAdminLogeado(!adminLogeado)
  }

  function manejarUser(){
    setUsuarioLogeado(!usuarioLogeado)
  }


  return (
    <Router>
      <div>
        <Header/>
        <Nav petsCarrito={petsCarrito} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/login' element={<Login user={usuarioLogeado} admin={adminLogeado} setLogeadoAdmin={setAdminLogeado} setLogeadoUser={setUsuarioLogeado}/>}/>
          <Route path="/about" element={<About />} />
          <Route path="/pets01" element={<PetsContainer/>} />
          {/*<Route path="/carrito" element={<Carrito petsCarrito={petsCarrito} funcionBorrar={borrarPetCarrito} usuarioLogeado={usuarioLogeado} /> } />*/} 
          <Route path="/carrito" element={<CarritoContainer usuarioLogeado={usuarioLogeado} />} />
          <Route path="/contacto" element={<Contacto />} />
          <Route path="/pets01/:id" element={<PetDetalle funcionCarrito={funcionCarrito} />} />
          <Route path='/admin' element={adminLogeado ? <Admin/> : <Navigate to={"/login"} replace/>} />
          <Route path="/adopcion" element={<AdopcionForm />} />n
        </Routes>
      </div>
    </Router>
  )
}

export default App