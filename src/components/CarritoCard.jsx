import "../styles/Carrito.css";

function CarritoCard({ pet, funcionDisparadora }) {
  function borrarDelCarrito() {
    console.log("Paso 1");
    funcionDisparadora(pet.id);
  }

  return (
    <div className="carrito-card">
      <h3 className="carrito-pet" style={{ color: "black" }}>{pet.nombre}</h3>
      <p className="descripcion-carrito" style={{ color: "grey" }}>{pet.descripcion}</p>
      <img className="carrito-image" src={pet.imagen} alt={pet.nombre} />
      <span style={{ color: "black" }}>{pet.cantidad}</span>
      <div>
        <p style={{ color: "black" }}>Precio unitario</p>
        <span style={{ color: "black" }}>{pet.price} $</span>
      </div>
      <div>
        <p style={{ color: "black" }}>...</p>
        <span style={{ color: "black" }}>{(pet.cantidad * pet.price).toFixed(2)} $</span>
      </div>
      <button className="carrito-boton" onClick={borrarDelCarrito}>X</button>
    </div>
  );
}

export default CarritoCard;