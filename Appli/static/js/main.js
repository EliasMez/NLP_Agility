/* Sélection des éléments HTML */
let link = document.getElementById('link');
let burger = document.getElementById('burger');
let ul = document.querySelectorAll("nav > .listnav");


/* gestionnaire d'événement sur le a#link pour venir changer l'attribution de la classe .open à la ul et au span#burger */
link.addEventListener('click', function(e) {
  e.preventDefault()
  burger.classList.toggle('open');
  for (element of ul) {
    element.classList.toggle('close');
  }
})