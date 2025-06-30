import "../styles/Login.css"

export default function Login({setLogeadoUser, setLogeadoAdmin, user, admin} ){

    return(
        <div className="login-container">
            <button className="login-button" onClick={setLogeadoUser}>
                {user ? "Cerrar sesión" : "Iniciar sesión"}
            </button>
            <button className="login-button" onClick={setLogeadoAdmin}>
                {admin ? "Cerrar sesión Admin" : "Iniciar sesión Admin"}
            </button>
        </div>

    );
}