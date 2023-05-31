// Variable global que lleva la cuenta de cuántos campos se han añadido hasta el momento
var membersCount = 1;

// Variable global que recoge la fecha de apertura anterior de la comisión para dar el aviso o no
let fechaAperturaAnterior = document.getElementById("fecha_apertura").value;

function addMembersCreate() {
  /*
  Función que añade nuevo campos para añadir miembros a la comisión en el formulario.
  Esta función se utiliza en la vista de crear una comisión.
  (Crear comisión)
  */

  // Obtenemos el último select creado
  var lastSelect = document.getElementById("member-" + (membersCount - 1));

  // Sólo dejamos añadir uno nuevo si ya ha seleccionado un miembro en el select actual
  if (lastSelect.value === "") {
    Swal.fire({
      text: "Selecciona un miembro en el campo actual si quieres añadir más miembros",
      icon: "info",
      confirmButtonText: "Aceptar",
    });

    return;
  }

  // Creamos el nuevo select
  var newSelect = document.createElement("select");
  newSelect.setAttribute("id", "member-" + membersCount);
  newSelect.setAttribute("name", "miembros");
  newSelect.setAttribute("class", "form-control m-3 input-nombre");
  newSelect.setAttribute("onchange", "checkRepeatedMembers(this)");

  // Agregamos las mismas opciones del último select al nuevo select
  var options = lastSelect.options;
  for (var i = 0; i < options.length; i++) {
    var option = document.createElement("option");
    option.text = options[i].text; // Fernando
    option.value = options[i].value; // 1
    newSelect.add(option);
  }

  // Creamos nuevo campo para el cargo desempeñado
  var newCargo = document.createElement("input");
  newCargo.setAttribute("id", "member-" + membersCount);
  newCargo.setAttribute("name", "cargos");
  newCargo.setAttribute("class", "form-control m-3");
  newCargo.setAttribute("type", "text");
  newCargo.setAttribute("placeholder", "Cargo desempeñado");

  // Incrementamos el contador de miembros
  membersCount++;

  // Agregamos el nuevo select, el nuevo campo para el cargo y un salto de línea
  var formGroup = document.createElement("div");
  formGroup.setAttribute("class", "form-group d-flex align-items-center");
  formGroup.appendChild(newSelect);
  formGroup.appendChild(newCargo);

  // Borramos el anterior botón antes de crear el nuevo
  document.getElementById("add-member-button").remove();
  var button = document.createElement("button");
  button.setAttribute("type", "button");
  button.setAttribute("class", "btn");
  button.setAttribute("id", "add-member-button");
  button.innerHTML =
    '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" xmlns:xlink="http://www.w3.org/1999/xlink" enable-background="new 0 0 512 512" width="30" height="30"><g><g><path d="M15 0.645C7.085 0.645 0.645 7.085 0.645 15s6.44 14.355 14.355 14.355 14.355 -6.44 14.355 -14.355S22.915 0.645 15 0.645zm0 26.321c-6.598 0 -11.966 -5.367 -11.966 -11.966S8.402 3.035 15 3.035 26.965 8.402 26.965 15 21.598 26.965 15 26.965z"/><path d="M20.953 13.804h-4.758V9.046c0 -0.661 -0.532 -1.196 -1.196 -1.196s-1.196 0.532 -1.196 1.196v4.758H9.046c-0.661 0 -1.196 0.532 -1.196 1.196s0.532 1.196 1.196 1.196h4.758v4.758c0 0.661 0.532 1.196 1.196 1.196s1.196 -0.532 1.196 -1.196v-4.758h4.758c0.661 0 1.196 -0.532 1.196 -1.196s-0.532 -1.196 -1.196 -1.196z"/></g></g>';
  button.setAttribute("onclick", "addMembersCreate()");
  formGroup.appendChild(button);

  // Hacemos los append
  var formDiv = document.getElementById("members-form");
  formDiv.appendChild(formGroup);
  formDiv.appendChild(document.createElement("br"));
}

function addMembersUpdate() {
  /*
  Función que añade nuevo campos para añadir miembros a la comisión en el formulario.
  Esta función se utiliza en la vista de actualizar una comisión
  (Actualizar comisión)
  */

  // Obtenemos el último select creado
  var lastSelect = document.getElementById("member-" + (membersCount - 1));

  // Sólo dejamos añadir uno nuevo si ya ha seleccionado un miembro en el select actual
  if (lastSelect.value === "") {
    Swal.fire({
      text: "Selecciona un miembro en el campo actual si quieres añadir más miembros",
      icon: "info",
      confirmButtonText: "Aceptar",
    });

    return;
  } else if (
    document.getElementsByName("fecha_incorporacion_nuevo_miembro")[
      membersCount - 1
    ].value === ""
  ) {
    // Al actualizar solo dejamos añadir uno nuevo si ha puesto una fecha de incorporación para el anterior
    Swal.fire({
      text: "Establece una fecha de incorporación para el miembro actual si quieres añadir más miembros",
      icon: "info",
      confirmButtonText: "Aceptar",
    });

    return;
  }

  // Creamos el nuevo select
  var newSelect = document.createElement("select");
  newSelect.setAttribute("class", "form-control input-nombre");
  newSelect.setAttribute("id", "member-" + membersCount);
  newSelect.setAttribute("name", "miembros");
  newSelect.setAttribute(
    "onchange",
    "checkRepeatedMembers(this); setNewMemberId(this); assignCurrentDate(this)"
  );

  // Agregamos las mismas opciones del último select al nuevo select
  var options = lastSelect.options;
  for (var i = 0; i < options.length; i++) {
    var option = document.createElement("option");
    option.text = options[i].text; // Fernando
    option.value = options[i].value; // 1
    newSelect.add(option);
  }

  // Incrementamos el contador de miembros
  membersCount++;

  // Agregamos el nuevo select y un salto de línea
  var formGroup = document.createElement("div");
  formGroup.setAttribute("class", "form-group d-flex align-items-center");
  formGroup.appendChild(newSelect);

  // Creamos los inputs de la fecha de incorporación, fecha de baja y cargo desempeñado
  var newFechaIncorporacion = document.createElement("input");
  newFechaIncorporacion.setAttribute("class", "form-control mx-2 input-fecha");
  newFechaIncorporacion.setAttribute(
    "name",
    "fecha_incorporacion_nuevo_miembro"
  );
  newFechaIncorporacion.setAttribute("type", "text");
  newFechaIncorporacion.setAttribute("placeholder", "Fecha de incorporación");
  newFechaIncorporacion.setAttribute("onfocus", "(this.type='date')");
  newFechaIncorporacion.setAttribute("onblur", "(this.type='text')");
  newFechaIncorporacion.setAttribute(
    "onchange",
    "checkDate(this, document.getElementsByName('fecha_apertura')[0].value); validateIncorporationDate(this)"
  );

  var newFechaBaja = document.createElement("input");
  newFechaBaja.setAttribute("class", "form-control mx-2 input-fecha");
  newFechaBaja.setAttribute("name", "fecha_baja_nuevo_miembro");
  newFechaBaja.setAttribute("type", "text");
  newFechaBaja.setAttribute("placeholder", "Fecha de baja");
  newFechaBaja.setAttribute("onfocus", "(this.type='date')");
  newFechaBaja.setAttribute("onblur", "(this.type='text')");
  newFechaBaja.setAttribute(
    "onchange",
    "checkDate(this, document.getElementsByName('fecha_apertura')[0].value); disableUnsubscribeReason(this);"
  );

  var newCargo = document.createElement("input");
  newCargo.setAttribute("class", "form-control mx-2 input-cargo");
  newCargo.setAttribute("name", "cargo_nuevo_miembro");
  newCargo.setAttribute("type", "text");
  newCargo.setAttribute("placeholder", "Cargo desempeñado");

  var newMotivoBaja = document.createElement("input");
  newMotivoBaja.setAttribute(
    "class",
    "form-control mx-2 input-motivoBaja isDisabled"
  );
  newMotivoBaja.setAttribute("name", "motivo_baja_nuevo_miembro");
  newMotivoBaja.setAttribute("type", "text");
  newMotivoBaja.setAttribute("placeholder", "Motivo de baja");

  formGroup.appendChild(newCargo);
  formGroup.appendChild(newFechaIncorporacion);
  formGroup.appendChild(newFechaBaja);
  formGroup.appendChild(newMotivoBaja);

  // Borramos el anterior botón antes de crear el nuevo
  document.getElementById("add-member-button").remove();
  var button = document.createElement("button");
  button.setAttribute("type", "button");
  button.setAttribute("class", "btn");
  button.setAttribute("id", "add-member-button");
  button.innerHTML =
    '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" xmlns:xlink="http://www.w3.org/1999/xlink" enable-background="new 0 0 512 512" width="30" height="30"><g><g><path d="M15 0.645C7.085 0.645 0.645 7.085 0.645 15s6.44 14.355 14.355 14.355 14.355 -6.44 14.355 -14.355S22.915 0.645 15 0.645zm0 26.321c-6.598 0 -11.966 -5.367 -11.966 -11.966S8.402 3.035 15 3.035 26.965 8.402 26.965 15 21.598 26.965 15 26.965z"/><path d="M20.953 13.804h-4.758V9.046c0 -0.661 -0.532 -1.196 -1.196 -1.196s-1.196 0.532 -1.196 1.196v4.758H9.046c-0.661 0 -1.196 0.532 -1.196 1.196s0.532 1.196 1.196 1.196h4.758v4.758c0 0.661 0.532 1.196 1.196 1.196s1.196 -0.532 1.196 -1.196v-4.758h4.758c0.661 0 1.196 -0.532 1.196 -1.196s-0.532 -1.196 -1.196 -1.196z"/></g></g>';
  button.setAttribute("onclick", "addMembersUpdate()");
  formGroup.appendChild(button);

  // Hacemos los append
  var formDiv = document.getElementById("members-form");
  formDiv.appendChild(formGroup);
  formDiv.appendChild(document.createElement("br"));
}

function checkRepeatedMembers(select) {
  /*
  Función que evita que en un select se seleccione
  dos veces el mismo miembro
  (Actualizar comisión / Crear comisión)
  */

  var selectedValue = select.value;

  // Recorremos todos los select que tenemos
  // Obtenemos todos los select que tienen un id que empieza por "member-<id>"
  const allSelects = document.querySelectorAll('[id^="member-"]');

  // Recorremos todos los selects
  for (var i = 0; i < allSelects.length; i++) {
    var currentSelect = allSelects[i];
    if (currentSelect !== select) {
      // Comprobamos si el valor seleccionado en el select actual ya está seleccionado en otro select
      if (currentSelect.value === selectedValue) {
        Swal.fire({
          text: "El miembro seleccionado ya ha sido añadido",
          icon: "info",
          confirmButtonText: "Aceptar",
        });
        select.value = ""; // Desmarcamos la opción seleccionada
        break;
      }
    }
  }
}

function setNewMemberId(select) {
  /*
  Función que será el controlador de eventos del select al seleccionar una opción.
  Es decir, cuando se seleccione una opción esta función se encargará de poner a los
  inputs de cargo, fecha_incorporacion, fecha_baja y motivo_baja como 'id' el siguiente formato:
  '{id_miembro}-cargo_nuevo_miembro'
  '{id_miembro}-fecha_incorporacion_nuevo_miembro',
  '{id_miembro}-fecha_baja_nuevo_miembro',
  '{id_miembro}-motivo_baja_nuevo_miembro'
  (Actualizar comisión)
  */

  // Obtenemos el valor de la opción que ha seleccionado el usuario
  var idMiembro = select.value; // Nos devuelve la ID del miembro

  //console.log(selectedValue);
  // Establecemos la ID a los campos
  const inputCargo = document.getElementsByName("cargo_nuevo_miembro")[
    membersCount - 1
  ];
  const inputFechaIncorporacion = document.getElementsByName(
    "fecha_incorporacion_nuevo_miembro"
  )[membersCount - 1];
  const inputFechaBaja = document.getElementsByName("fecha_baja_nuevo_miembro")[
    membersCount - 1
  ];
  const inputMotivoBaja = document.getElementsByName(
    "motivo_baja_nuevo_miembro"
  )[membersCount - 1];

  inputCargo.setAttribute("id", idMiembro + "-cargo_nuevo_miembro");
  inputFechaIncorporacion.setAttribute(
    "id",
    idMiembro + "-fecha_incorporacion_nuevo_miembro"
  );
  inputFechaBaja.setAttribute("id", idMiembro + "-fecha_baja_nuevo_miembro");
  inputMotivoBaja.setAttribute("id", idMiembro + "-motivo_baja_nuevo_miembro");
}

function checkDate(fechaIntroducida, fechaApertura) {
  /*
  Función que comprobará que la fecha de incorporación o de baja de ningún miembro
  sea anterior a la fecha de apertura de la comisión.
  Es una función genérica que recibe una fecha de incorporación y una fecha de apertura.
  Ésta será llamada en el onchange de cada input de fecha_incorporacion
  (Actualizar comisión)
  */
  var fechaIntroducidaObj = new Date(fechaIntroducida.value);
  var fechaAperturaObj = new Date(fechaApertura);
  //console.log(fechaIncorporacionObj);
  //console.log(fechaAperturaObj);

  if (fechaIntroducidaObj < fechaAperturaObj) {
    // Vemos si estamos controlando una fecha de incorporación o de baja para mostrar un mensaje u otro
    if (fechaIntroducida.name.includes("fecha_incorporacion")) {
      Swal.fire({
        text: "La fecha de incorporación no puede ser anterior a la fecha de apertura",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
    } else if (fechaIntroducida.name.includes("fecha_baja")) {
      Swal.fire({
        text: "La fecha de baja no puede ser anterior a la fecha de apertura",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
    }

    if (fechaIntroducida.defaultValue === "") {
      // Creamos la fecha actual con el formato que nos pide HTML para el formulario (yyyy-MM-dd)
      const date = new Date(Date.now());
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      const formattedDate = `${year}-${month}-${day}`;

      fechaIntroducida.value = formattedDate;
    } else {
      fechaIntroducida.value = fechaIntroducida.defaultValue;
    }
    return false;
  }

  return true;
}

function validateIncorporationDate(fechaIncorporacion) {
  /*
  Función que valida que ninguna fecha de incorporación de ningún miembro sea vacía y no
  pueda enviarse el formulario así
  (Actualizar comisión)
  */

  // Creamos la fecha actual con el formato que nos pide HTML para el formulario (yyyy-MM-dd)
  const date = new Date(Date.now());
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const formattedDate = `${year}-${month}-${day}`;

  const inputType = fechaIncorporacion.name;

  if (inputType.includes("fecha_incorporacion_modificada")) {
    // Si es un input de la fecha de incorporación de un miembro existente NUNCA podrá dejarse en blanco
    if (fechaIncorporacion.value == "") {
      Swal.fire({
        text: "Debes establecer una fecha de incorporación para el miembro",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
      fechaIncorporacion.value = formattedDate;
    }
  } else if (inputType.includes("fecha_incorporacion_nuevo_miembro")) {
    // Si es un input de la fecha de incorporación de un miembro que se quiere añadir
    // como nuevo puede dejarse en blanco si todavía no ha seleccionado miembro

    // Debemos establecer para ese campo una por defecto
    // ¿Justo al introducirse un miembro en el campo en una función asignada al onchange del select?

    // Obtenemos el select asociado a ese input
    // Primero obtenemos la ID del miembro seleccionado a través de la id de la fecha de incorporación,
    // ya que ésta contiene la ID del miembro seleccionado
    var selectedMember = fechaIncorporacion.id.split("-")[0];

    // Ahora recorremos todos los select que tenemos y obtenemos el select que tenga seleccionado
    // la ID obtenida
    const allSelects = document.querySelectorAll('[id^="member-"]');
    var memberSelect;
    for (var i = 0; i < allSelects.length; i++) {
      var currentSelect = allSelects[i];
      if (currentSelect.value === selectedMember) {
        memberSelect = currentSelect;
      }
    }
    //var lastSelect = document.getElementById("member-" + (membersCount - 1));
    //console.log(membersCount - 1);

    if (fechaIncorporacion.value == "" && memberSelect.value != "") {
      Swal.fire({
        text: "Debes establecer una fecha de incorporación para el miembro",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
      fechaIncorporacion.value = formattedDate;
    }
  }
}

function assignCurrentDate(selectMiembro) {
  /*
  Función que se encargará de que cuando el usuario seleccione un miembro nuevo para añadirlo a la comisión,
  colocar por defecto en su fecha de incorporación la fecha actual.
  Es usada para que el usuario no envíe la fecha de incorporación como vacía
  (Actualizar comisión)
  */

  // Creamos la fecha con el formato que nos pide HTML para el formulario (yyyy-MM-dd)
  const date = new Date(Date.now());
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const formattedDate = `${year}-${month}-${day}`;

  if (selectMiembro.value != "") {
    // Se ha seleccionado un miembro
    document.getElementsByName("fecha_incorporacion_nuevo_miembro")[
      membersCount - 1
    ].value = formattedDate;
  } else {
    document.getElementsByName("fecha_incorporacion_nuevo_miembro")[
      membersCount - 1
    ].value = "";
  }
}

function showAdviceOpeningDate() {
  /*
  Función que muestra una advertencia si el usuario modifica la fecha de apertura a una fecha
  posterior a la fecha de apertura original.
  (Actualizar comisión)
  */
  let fechaAperturaNueva = document.getElementById("fecha_apertura").value;

  if (fechaAperturaNueva > fechaAperturaAnterior) {
    Swal.fire({
      title: "Atención",
      text: "Si algún miembro ya perteneciente a esta comisión tiene su fecha de incorporación anterior a la nueva fecha de apertura, su fecha de incorporación se establecerá como la nueva fecha de apertura.",
      icon: "warning",
      confirmButtonText: "De acuerdo",
    });
  }

  fechaAperturaAnterior = fechaAperturaNueva;
}

function disableUnsubscribeReason(fechaBaja, motivoBaja) {
  /*
  Función que deshabilita el campo "motivo de baja" si no se hay ya
  establecida una fecha de baja para ese miembro.

  Recibe como argumentos:
    - Fecha de baja introducida para ese miembro
    - Campo "motivo_baja" para ese miembro (Opcional)
  (Actualizar comisión) 
  */

  // Si la función es llamada por un campo de un nuevo miembro el parámetro
  // 'motivoBaja' no será pasado y se hallará el campo de motivo de baja de ese
  // miembro dentro de la función
  motivoBaja = motivoBaja || 0;

  if (motivoBaja === 0) {
    // Hallamos el campo de motivo de baja para ese miembro a partir de la ID
    const idMiembro = fechaBaja.id.split("-")[0];
    if (idMiembro === "") {
      // Evitamos que introduzca la fecha de baja antes de indicar el miembro
      Swal.fire({
        text: "Por favor, indique el miembro antes de establecer la fecha de baja",
        icon: "info",
        confirmButtonText: "Aceptar",
      });
      fechaBaja.value = "";
      return;
    }
    motivoBaja = document.getElementById(
      idMiembro + "-motivo_baja_nuevo_miembro"
    );
  }

  let fechaBajaObj = fechaBaja.value;
  let motivoBajaClass = motivoBaja.getAttribute("class");

  if (fechaBajaObj === "") {
    // Desactivamos el campo si no hay fecha de baja
    let motivoBajaNewClass = motivoBajaClass + " isDisabled";
    motivoBaja.setAttribute("class", motivoBajaNewClass);
  } else {
    // Lo activamos si introduce una fecha de baja
    // Sólo le quitamos la clase "isDisabled"
    let motivoBajaNewClass = motivoBajaClass.replace(/\bisDisabled\b/, "");
    motivoBaja.setAttribute("class", motivoBajaNewClass);
  }
}
