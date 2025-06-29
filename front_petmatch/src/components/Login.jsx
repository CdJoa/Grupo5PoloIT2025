import { useState } from "react";
import "../styles/Login.css";

// ⭐ ESTA FUNCIÓN VA AL INICIO DEL ARCHIVO:
// Función para obtener el valor de una cookie por nombre
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

export default function Login({ setLogeadoUser, setLogeadoAdmin, user, admin }) {
  const [showFormUser, setShowFormUser] = useState(false);
  const [showFormAdmin, setShowFormAdmin] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  // ⭐ ESTA FUNCIÓN SE EDITÓ PARA AGREGAR EL CSRF TOKEN
  // Función para hacer login a Django
  const loginDjango = async (isAdmin) => {
    try {
      const csrftoken = getCookie("csrftoken"); // ⭐ OBTENEMOS EL CSRF TOKEN

      const res = await fetch("http://127.0.0.1:8000/api/login/", {
        method: "POST",
        credentials: "include", // para usar cookies de sesión
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken, // ⭐ AGREGAMOS EL HEADER CSRF
        },
        body: JSON.stringify({ username, password }),
      });

      if (res.ok) {
        setError(null);
        if (isAdmin) {
          setLogeadoAdmin(true);
          setLogeadoUser(false);
        } else {
          setLogeadoUser(true);
          setLogeadoAdmin(false);
        }
        setShowFormUser(false);
        setShowFormAdmin(false);
      } else {
        const data = await res.json();
        setError(data.error || "Error al iniciar sesión");
      }
    } catch {
      setError("No se pudo conectar con el servidor");
    }
  };

  // Función logout, limpia estados y avisa a Django
  const logoutDjango = async (isAdmin) => {
    await fetch("http://127.0.0.1:8000/logout/", {
      method: "POST",
      credentials: "include",
    });
    if (isAdmin) setLogeadoAdmin(false);
    else setLogeadoUser(false);
  };

  return (
    <div className="login-container">
      {/* Botón usuario */}
      {user ? (
        <button className="login-button" onClick={() => logoutDjango(false)}>
          Cerrar sesión
        </button>
      ) : (
        <>
          <button
            className="login-button"
            onClick={() => {
              setShowFormUser(!showFormUser);
              setShowFormAdmin(false);
              setError(null);
            }}
          >
            Iniciar sesión
          </button>
          {showFormUser && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                loginDjango(false);
              }}
            >
              <input
                type="text"
                placeholder="Usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="password"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button type="submit">Entrar</button>
              {error && <p style={{ color: "red" }}>{error}</p>}
            </form>
          )}
        </>
      )}

      {/* Botón admin */}
      {admin ? (
        <button className="login-button" onClick={() => logoutDjango(true)}>
          Cerrar sesión Admin
        </button>
      ) : (
        <>
          <button
            className="login-button"
            onClick={() => {
              setShowFormAdmin(!showFormAdmin);
              setShowFormUser(false);
              setError(null);
            }}
          >
            Iniciar sesión Admin
          </button>
          {showFormAdmin && (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                loginDjango(true);
              }}
            >
              <input
                type="text"
                placeholder="Admin usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <input
                type="password"
                placeholder="Admin contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <button type="submit">Entrar Admin</button>
              {error && <p style={{ color: "red" }}>{error}</p>}
            </form>
          )}
        </>
      )}
    </div>
  );
}