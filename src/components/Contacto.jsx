import "../styles/Contacto.css";
import Footer from './Footer';


function Contacto() {
  return (
    <>
      <div className="contacto-container">
        <h2>Contacto</h2>
        <p>Podés contactarnos completando el siguiente formulario o a través de nuestros canales directos:</p>

        <form className="contacto-form">
          <label htmlFor="nombre">Nombre</label>
          <input type="text" id="nombre" placeholder="Tu nombre" required />

          <label htmlFor="email">Email</label>
          <input type="email" id="email" placeholder="tu@email.com" required />

          <label htmlFor="mensaje">Mensaje</label>
          <textarea id="mensaje" placeholder="Escribí tu mensaje aquí..." rows="5" required></textarea>

          <button type="submit">Enviar</button>
        </form>
      </div>

      <Footer/>
    </>
  );
}

export default Contacto