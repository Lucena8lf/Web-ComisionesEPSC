// Función principal que se encargará de controlar el switch
(function () {
  // Obtenemos todos los switches que tienen un id que empieza por "miembroSwitch"
  const switches = document.querySelectorAll('[id^="miembroSwitch"]');

  // Función auxiliar para insertar tras un elemento
  function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }

  /* Para aprobar una cosa diferente crearemos dos funciones en función si el switch está activado o desactivado */
  function activarMiembro() {
    // Creamos un nuevo elemento <p>
    const para = document.createElement("p");
    para.setAttribute("id", "texto_prueba");

    // Creamos un texto de nodo. Esto es para añadir texto a ese elemento <p> que hemos creado
    const node = document.createTextNode("El usuario está activado");

    // Le agregamos el texto al elemento <p>
    para.appendChild(node);

    // Finalmente añadimos ese elemento a otro elemento que queramos o aparte. En nuestro caso lo insertamos después del div del switch
    const current_div = document.getElementById("switch_div");

    insertAfter(current_div, para);
  }

  function activarMiembroReal() {
    // Activamos el miembro accediendo a la URL
    fetch("https://swapi.dev/api/films/1/")
      .then((res) => res.json())
      .then((res) => console.log(res.title));
  }

  function desactivarMiembro() {
    // Eliminamos el div
    const elmnt = document.getElementById("texto_prueba");
    elmnt.remove();
  }

  function onToggleMode(switchElement) {
    // Esta función será la que maneje los eventos del switch
    // Es decir, si está activado significa que ese miembro está activo, por lo que habrá que desactivarlo, y viceversa
    // En nuestro caso, si está activado significa que está en modo claro, por lo que habrá que ponerlo todo oscuro

    // Obtenemos el id del miembro del switch actual
    const miembroId = switchElement.id.slice(13); // elimina "miembroSwitch" del id
    console.log(miembroId);

    // Obtenemos el estado actual del switch
    const switchState = switchElement.checked;

    console.log("Holaa");
    if (switchState) {
      let confirmar = confirm(
        "Estás a punto de activar un miembro. ¿Deseas hacerlo?"
      );
      if (confirmar) {
        alert("ACTIVADO!");
      } else {
        mySwitch.checked = false;
      }
    } else {
      console.log("Estoy desactivado");
      alert("DESACTIVADO");
    }
  }

  function setup() {
    // Función inicial
    // Esta función debe comprobar en que estado se encuentra el miembro (activo o no activo) para ver en que posición poner el switch
    // Aquí para probarlo lo haremos con el modo claro/oscuro

    // Recorremos todos los switches que tenemos y le añadimos un manejador de evento para 'change'
    console.log(switches);
    if (switches) {
      switches.forEach((switchElement) => {
        //switchElement.addEventListener("change", onToggleMode(switchElement));
        switchElement.addEventListener("change", async () => {
          // Obtenemos el id del miembro del switch actual
          const miembroId = switchElement.id.slice(13); // elimina "miembroSwitch" del id

          // Obtenemos el estado actual del switch
          const switchState = switchElement.checked;

          if (!switchState) {
            // Si está activo y lo pulsa significa que lo quiere desactivar
            //console.log("Está activo");
            let confirmar = confirm(
              "Estás a punto de desactivar un miembro. ¿Deseas hacerlo?"
            );
            if (confirmar) {
              // TO DO
              const response = await fetch(
                `/miembros/${miembroId}/desactivar`,
                {
                  method: "POST",
                }
              );

              if (response.ok) {
                console.log("Miembro actualizado correctamente");
                alert("DESACTIVADO!");
              } else {
                console.error("Error al actualizar el miembro");
              }
            } else {
              switchElement.checked = true;
            }
          } else {
            // Si está desactivado y lo pulsa significa que lo quiere activar
            let confirmar = confirm(
              "Estás a punto de activar un miembro. ¿Deseas hacerlo?"
            );
            if (confirmar) {
              // TO DO
              const response = await fetch(`/miembros/${miembroId}/activar`, {
                method: "POST",
              });

              if (response.ok) {
                console.log("Miembro actualizado correctamente");
                alert("ACTIVADO!");
              } else {
                console.error("Error al actualizar el miembro");
              }
            } else {
              switchElement.checked = false;
            }
          }

          // Hacer algo con el estado del switch y el id del miembro
          /*
          console.log(
            `El switch del miembro ${miembroId} está ${
              switchState ? "activado" : "desactivado"
            }`
          );
          */
        });
      });
    }
  }

  setup();
})();
