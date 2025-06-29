import "../styles/Carrito.css"
import { useEffect, useState } from "react";
import CarritoCard from "./CarritoCard.jsx";
import { Navigate } from "react-router-dom";

// Obtener el CSRF desde las cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrfToken = getCookie("csrftoken");

export default function Carrito({ petsCarrito, funcionBorrar, usuarioLogeado }) {
  function funcionDisparadora(id) {
    funcionBorrar(id);
  }

  // Confirmar adopción (envía al backend)
  function confirmarAdopcion() {
    fetch("http://127.0.0.1:8000/api/adopcion/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
      body: JSON.stringify({ mascotas: petsCarrito }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("¡Adopción confirmada!");
        // Podés limpiar el carrito aquí si querés:
        // funcionBorrar("todo")
      })
      .catch((err) => {
        console.error("Error al confirmar adopción:", err);
        alert("Hubo un error al procesar la adopción.");
      });
  }

  // Si no está logueado, redirige al login
  if (!usuarioLogeado) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="carrito-container">
      {petsCarrito.length > 0 ? (
        <>
          {petsCarrito.map((pet) => (
            <div key={pet.id} className="carrito-titulos">
              <h2 className="carrito-titulo-pet">{pet.nombre}</h2>
              <h2 className="carrito-titulo-descrip">{pet.descripcion}</h2>
              <p><strong>Especie:</strong> {pet.especie}</p>
              <p><strong>Provincia:</strong> {pet.provincia}</p>
              <p><strong>Localidad:</strong> {pet.localidad}</p>

              <CarritoCard
                pet={pet}
                funcionDisparadora={funcionDisparadora}
              />
            </div>
          ))}
          <button onClick={confirmarAdopcion} className="btn-confirmar">
            Confirmar adopción
          </button>
        </>
      ) : (
        <p>Carrito vacío</p>
      )}
    </div>
  );
}