function validateDates(fechaIntroducida) {
  /*
    Función encargada de asegurar que no se introduzcan fechas incoherentes en el formulario al generar
    comisiones. Si es llamada por la fecha de inicio comprobará que si existe ya una fecha de fin ésta
    no sea superior. Por otro lado, si es llamada por la fecha de fin comprobará que si ya existe una fecha
    de inicio ésta no sea superior
  */

  // Mediante el id vemos que fecha llama a la función
  const fecha = fechaIntroducida.id;

  if (fecha === "fecha_inicio") {
    // Comprobamos la fecha de fin
    const fechaFin = document.getElementById("fecha_fin");
    if (fechaFin.value !== "" && fechaIntroducida.value > fechaFin.value) {
      Swal.fire({
        text: "La fecha de inicio no puede ser posterior a la fecha de fin",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
      fechaIntroducida.value = fechaIntroducida.defaultValue;
    }
  } else if (fecha === "fecha_fin") {
    // Comprobamos la fecha de inicio
    const fechaInicio = document.getElementById("fecha_inicio");
    if (
      fechaInicio.value !== "" &&
      fechaIntroducida.value < fechaInicio.value
    ) {
      Swal.fire({
        text: "La fecha de fin no puede ser anterior a la fecha de inicio",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
      fechaIntroducida.value = fechaIntroducida.defaultValue;
    }
  }
}

function handleSubmit(event) {
  /*
    Función que muestra un mensaje cuando envía el formulario del informe y comprueba que todos los
    campos estén rellenos para evitar abrir otra pestaña
  */

  // Comprobamos si los campos están rellenos
  const secretario = document.getElementById("secretario");
  const fechaInicio = document.getElementById("fecha_inicio");
  const fechaFin = document.getElementById("fecha_fin");

  if (
    secretario.value === "" ||
    fechaInicio.value === "" ||
    fechaFin.value === ""
  ) {
    event.preventDefault();
    Swal.fire({
      text: "Todos los campos deben estar rellenos para generar el informe",
      icon: "info",
      confirmButtonText: "Aceptar",
    });
  } else {
    // Obtenemos el div donde va el mensaje y lo mostramos ahí
    const messageDiv = document.getElementById("message");

    messageDiv.innerHTML = "¡Informe generado con éxito!";
    messageDiv.style.display = "block";

    setTimeout(function () {
      messageDiv.style.display = "none";
    }, 20000); // Ocultamos el mensaje después de 20 segundos
  }
}
