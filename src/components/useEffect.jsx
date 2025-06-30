import { useEffect } from "react";

useEffect(() => {
    console.log("Primera ejecución")
    // Código del efecto secundario
    return () => {
      // Limpieza del efecto             //(opcional)
    };
  }, []);