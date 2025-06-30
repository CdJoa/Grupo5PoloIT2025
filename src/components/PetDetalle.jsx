import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../styles/PetDetalle.css";
//import { dispararSweetBasico } from "../assets/SweetAlert";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { FaHeart, FaArrowLeft } from "react-icons/fa";


function PetDetalle({ funcionCarrito} ){
    const {id}= useParams();
    const [pet, setPet] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    
    useEffect(() => {
        // Fetch el detalle directo por id desde tu backend Django
    fetch(`http://127.0.0.1:8000/api/pets/${id}/`, {
      method: "GET",
      credentials: "include", // si usas sesiones o cookies, si no podés eliminar esta línea
    })
        .then((res) => {
        if (!res.ok) throw new Error("Mascota no encontrada");
        return res.json();
      })
      .then((data) => {
        console.log("Mascota recibida:", data);
        setPet(data);
        setCargando(false);
      })
      .catch((err) => {
        console.error("Error:", err);
        setError("Error al buscar la mascota");
        setCargando(false);
      });
  }, [id]);

  function agregarAlCarrito() {
    toast.success("🐾 La mascota fue agregada con éxito", {
      className: "mi-toast",
      bodyClassName: "mi-toast-body",
      autoClose: 2500,
    });
    funcionCarrito({ ...pet, cantidad: 1 }); // cantidad fija 1 para sumar al carrito
  }

  if (cargando) return <p>Cargando ...</p>;
  if (error) return <p>{error}</p>;
  if (!pet) return null;

  return (
    <div className="detalle-container">
      <img className="detalle-imagen" src={pet.imagen} alt={pet.nombre} />
      <div className="detalle-info">
        <h2>{pet.nombre}</h2>
        <p><strong>Descripción:</strong> {pet.descripcion}</p>
        <p><strong>Especie:</strong> {pet.especie}</p>
        <p><strong>Provincia:</strong> {pet.provincia}</p>
        <p><strong>Localidad:</strong> {pet.localidad}</p>
      </div>
      <div className="detalle-acciones">
        <FaArrowLeft
          className="detalle-icono volver"
          title="Volver"
          onClick={() => navigate(-1)}
        />
        <div
          className="adoptar-btn"
          onClick={agregarAlCarrito}
          title="Agregar al carrito"
        >
          <span className="adoptar-texto">¡Quiero Adoptar!</span>
          <FaHeart className="detalle-icono agregar" />
        </div>
      </div>
      <ToastContainer />
    </div>
  );
}

export default PetDetalle;