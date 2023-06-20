function inicializarCuadros() {
  var cuadros = document.querySelectorAll(".box");
  var info = document.getElementById("info");
  const textoIndex = document.getElementById("texto-index");

  // Recorremos todos los cuadros
  cuadros.forEach(function (cuadro) {
    if (!cuadro.classList.contains("box-informe")) {
      cuadro.addEventListener("click", function (evento) {
        evento.preventDefault(); // Evita que el enlace se abra
        var url = this.getAttribute("href"); // Obtiene el valor del atributo href
        // Borramos el texto que hay si existe y hacemos el iframe
        if (textoIndex) {
          textoIndex.style.display = "none";
        }
        const iframe = document.getElementById("iframe-index");
        iframe.setAttribute("src", url);

        // Si ha seleccionado la opción 'Exportar' no se crea el spinner sino que
        // se cambia el mensaje de bienvenida del cuadro
        if (cuadro.classList.contains("box-exportar")) {
          iframe.style.display = "none";
          const loadingMessage = document.getElementById("loading-message");
          // Metemos el HTML dentro de ese div
          loadingMessage.innerHTML =
            '<span class="blink" id="texto-csv">Generando fichero CSV...</span>';

          // Llamamos a la función JS para que muestre el mensaje
          showLoadingText();
        } else {
          iframe.style.display = "";
          if (document.getElementById("texto-csv")) {
            document.getElementById("texto-csv").style.display = "none";
          }
          // Creamos el spinner
          // Primero obtenemos el padre del iframe
          const parent = iframe.parentNode;

          // Creamos el nuevo div que será el spinner
          const spinnerDiv = document.createElement("div");
          spinnerDiv.classList.add("spinner");
          spinnerDiv.id = "spinner";

          // Agregamos el div justo después del iframe
          parent.insertAdjacentElement("afterend", spinnerDiv);

          // Función para eliminar el spinner cuando el iframe cargue la información
          iframe.onload = function () {
            var spinner = document.getElementById("spinner");
            //spinner.style.display = "none";
            spinner.remove();
          };
        }
      });
    }
  });
}

window.onload = function () {
  inicializarCuadros();
};

function showLoadingText() {
  // Mostrar mensaje de carga
  document.getElementById("loading-message").style.display = "block";

  // Iniciamos efecto de parpadeo durante 3 segundos
  var messageElement = document.querySelector(".blink");
  var timeoutDuration = 3000;
  var timer = setTimeout(function () {
    // Ocultamos el mensaje de carga
    document.getElementById("texto-csv").innerHTML =
      "¡Fichero CSV generado! ✔️";
  }, timeoutDuration);

  function stopBlinking() {
    clearTimeout(timer);
    messageElement.classList.remove("blink");
  }

  // Detenemos el parpadeo después de 4 segundos
  var stopBlinkingTimeout = 4000;
  setTimeout(stopBlinking, stopBlinkingTimeout);
}
