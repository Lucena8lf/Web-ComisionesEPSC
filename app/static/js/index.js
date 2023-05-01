/*

document.querySelectorAll(".box").forEach((box) => {
  box.addEventListener("click", (e) => {
    e.preventDefault();
    let info = document.getElementById("info");
    info.innerHTML = "<p>Cargando información...</p>";
    fetch(e.target.href)
      .then((response) => response.text())
      .then((html) => {
        info.innerHTML = html;
      });
  });
});
*/
//alert("hola");
//import { mostrarCuadroMiembro } from "./miembros_index";

function inicializarCuadros() {
  var cuadros = document.querySelectorAll(".box");
  var info = document.getElementById("info");

  // Recorremos todos los cuadros
  cuadros.forEach(function (cuadro) {
    cuadro.addEventListener("click", function (evento) {
      evento.preventDefault(); // Evita que el enlace se abra
      var url = this.getAttribute("href"); // Obtiene el valor del atributo href
      // Borramos el texto que hay si existe y hacemos el iframe
      if (document.getElementById("texto-index")) {
        document.getElementById("texto-index").remove();
      }
      const iframe = document.getElementById("iframe-index");
      iframe.setAttribute("src", url);

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
      /*
      fetch(href)
        .then((response) => response.text())
        .then((html) => {
          info.innerHTML = html;
        }); // Carga la vista en el div info
        */
    });
  });
}

window.onload = function () {
  inicializarCuadros();
};
