// Función inicial
// Esta función debe comprobar en que estado se encuentra el miembro (activo o no activo) para ver en que posición poner el switch

// Obtenemos todos los switches que tienen un id que empieza por "miembroSwitch"
const switches = document.querySelectorAll('[id^="miembroSwitch"]');

// Recorremos todos los switches que tenemos y le añadimos un manejador de evento para 'change'
if (switches) {
  switches.forEach((switchElement) => {
    switchElement.addEventListener("change", async () => {
      // Obtenemos el id del miembro del switch actual
      const miembroId = switchElement.id.slice(13); // eliminamos "miembroSwitch" del id

      // Obtenemos el estado actual del switch
      const switchState = switchElement.checked;

      if (!switchState) {
        // Si está activo y lo pulsa significa que lo quiere desactivar
        Swal.fire({
          title: "¿Deseas hacerlo?",
          text: "Estás a punto de desactivar el miembro",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Desactivar",
          cancelButtonText: "Cancelar",
        }).then(async (result) => {
          if (result.isConfirmed) {
            const response = await fetch(`/miembros/${miembroId}/desactivar`, {
              method: "POST",
            });
            if (response.ok) {
              Swal.fire(
                "¡Desactivado!",
                "El miembro ha sido desactivado con éxito",
                "success"
              );
              // Modificamos el tag
              let spanActivo = document.getElementById("tag-activo");
              spanActivo.innerHTML = "❌";
              spanActivo.id = "tag-inactivo";
            } else {
              Swal.fire(
                "Error",
                "Se ha producido un error al desactivar el miembro",
                "error"
              );
              switchElement.checked = true;
            }
          } else {
            Swal.fire("Cancelado", "El miembro sigue activo", "error");
            switchElement.checked = true;
          }
        });
      } else {
        // Si está desactivado y lo pulsa significa que lo quiere activar
        Swal.fire({
          title: "¿Deseas hacerlo?",
          text: "Estás a punto de activar el miembro",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Activar",
          cancelButtonText: "Cancelar",
        }).then(async (result) => {
          if (result.isConfirmed) {
            const response = await fetch(`/miembros/${miembroId}/activar`, {
              method: "POST",
            });

            if (response.ok) {
              Swal.fire(
                "¡Activado!",
                "El miembro ha sido activado con éxito",
                "success"
              );
              // Modificamos el tag
              let spanInactivo = document.getElementById("tag-inactivo");
              spanInactivo.innerHTML = "✔️";
              spanInactivo.id = "tag-activo";
            } else {
              Swal.fire(
                "Error",
                "Se ha producido un error al desactivar el miembro",
                "error"
              );
              switchElement.checked = false;
            }
          } else {
            Swal.fire("Cancelado", "El miembro sigue desactivado", "error");
            switchElement.checked = false;
          }
        });
      }
    });
  });
}
