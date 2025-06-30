import { useEffect, useState } from "react";
import Carrito from "./Carrito";

export default function CarritoContainer({ usuarioLogeado }) {
  const [petsCarrito, setPetsCarrito] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/carrito/", {
      credentials: "include", // para enviar cookies de sesión
    })
      .then(async (res) => {
        console.log('Status:', res.status);
        console.log('Content-Type:', res.headers.get('Content-Type'));

        if (!res.ok) {
          // Si no está autorizado, podés manejarlo aparte
          if (res.status === 401) {
            throw new Error("No autorizado. Por favor inicia sesión.");
          } else {
            throw new Error(`Error HTTP: ${res.status}`);
          }
        }

        // Intentar parsear JSON sólo si Content-Type es JSON
        const contentType = res.headers.get("Content-Type") || "";
        if (contentType.includes("application/json")) {
          return res.json();
        } else {
          // Si no es JSON, leer texto para debug
          const text = await res.text();
          throw new Error("Respuesta no es JSON: " + text);
        }
      })
      .then((data) => {
        setPetsCarrito(data);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setPetsCarrito([]);
      });
  }, []);

  function borrarPetCarrito(id) {
    fetch(`http://127.0.0.1:8000/api/carrito/${id}/`, {
      method: "DELETE",
      credentials: "include",
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Error al borrar: ${res.status}`);
        }
        setPetsCarrito((prev) => prev.filter((p) => p.id !== id));
      })
      .catch((err) => {
        console.error(err);
        alert("No se pudo borrar el ítem: " + err.message);
      });
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Carrito
      petsCarrito={petsCarrito}
      funcionBorrar={borrarPetCarrito}
      usuarioLogeado={usuarioLogeado}
    />
  );
}
