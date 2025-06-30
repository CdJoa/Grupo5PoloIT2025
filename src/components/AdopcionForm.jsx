import React, { useState } from "react";
import "../styles/AdopcionForm.css";
import Footer from "./Footer";

export default function AdopcionForm() {
  const [acepta, setAcepta] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!acepta) {
      alert("Debes aceptar los Términos y Condiciones");
      return;
    }
    alert("¡Formulario enviado!");
  };

  return (
    <>
      <div className="container my-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card adopcion-card">
              <div className="card-body">
                <h1 className="adopcion-title mb-3">
                  ¿Querés dar en adopción?
                </h1>
                <p className="adopcion-text mb-4">
                  Dar en adopción es un acto de amor y responsabilidad.
                  Asegúrate de que tu mascota recibirá cuidado, cariño y un
                  hogar seguro.
                </p>

                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label">
                      Nombre de la mascota
                    </label>
                    <input
                      type="text"
                      name="nombre"
                      className="form-control"
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Especie</label>
                    <select
                      name="especie"
                      className="form-select"
                      required
                    >
                      <option value="">Selecciona</option>
                      <option value="perro">Perro</option>
                      <option value="gato">Gato</option>
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Descripción</label>
                    <textarea
                      name="descripcion"
                      className="form-control"
                      rows="3"
                      required
                    ></textarea>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Provincia</label>
                    <input
                      type="text"
                      name="provincia"
                      className="form-control"
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Localidad</label>
                    <input
                      type="text"
                      name="localidad"
                      className="form-control"
                      required
                    />
                  </div>

                  <div className="form-check mb-3">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      checked={acepta}
                      onChange={() => setAcepta(!acepta)}
                      id="terminosCheck"
                    />
                    <label
                      className="form-check-label"
                      htmlFor="terminosCheck"
                    >
                      Acepto los{" "}
                      <span
                        className="link-terminos"
                        onClick={() => setShowModal(true)}
                      >
                        Términos y Condiciones
                      </span>
                    </label>
                  </div>

                  <button type="submit" className="btn-enviar w-100">
                    Enviar
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div
          className="modal fade show"
          style={{
            display: "block",
            backgroundColor: "rgba(0,0,0,0.5)",
          }}
        >
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  Términos y Condiciones
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                <p>
                  TÉRMINOS Y CONDICIONES DE ADOPCIÓN

Al ofrecer en adopción una mascota en PetMatch, el usuario declara ser su responsable legal y asegura que los datos proporcionados son veraces.

La mascota debe estar en buen estado de salud o con condiciones informadas de forma clara. No se permitirá solicitar pagos indebidos, salvo gastos veterinarios comprobables.

PetMatch no se responsabiliza por conflictos entre adoptantes y usuarios, pero podrá intervenir si es necesario.

Los datos personales se usan solo para gestionar adopciones y no se compartirán sin permiso. PetMatch podrá moderar o eliminar publicaciones que no cumplan estas reglas.

Al aceptar, el usuario confirma haber leído y aceptado estos términos. Es importante que leas todo antes de aceptar.
                </p>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn-enviar"
                  onClick={() => setShowModal(false)}
                >
                  Aceptar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </>
  );
}