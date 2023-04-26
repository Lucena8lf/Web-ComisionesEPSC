$(document).ready(function () {
  $('[data-bs-toggle="popover"]').popover({
    placement: "right", // Posiciona el cuadro de ayuda a la derecha del cursor
    trigger: "hover", // Se activa al pasar el mouse por encima
    html: true, // Permite utilizar HTML dentro del contenido del cuadro de ayuda
    template:
      '<div class="popover" role="tooltip"><div class="popover-arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
    // Define el formato del cuadro de ayuda
  });
});
