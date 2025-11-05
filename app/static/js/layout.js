//Funcion que controla las pestanas de inicio

function showContent(tabId) {
    // Ocultar todo el contenido
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => content.classList.remove('active'));

    // Quitar la clase activa de todas las pestañas
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Mostrar el contenido seleccionado
    document.getElementById(tabId).classList.add('active');

    // Activar la pestaña seleccionada
    event.target.classList.add('active');
}

// Carrusel de imágenes
// Selecciona los botones de navegación

let currentIndex = 0;

function moveCarousel(direction) {
    const carousel = document.querySelector('.carousel');
    const items = document.querySelectorAll('.carousel-item');
    const totalItems = items.length;

    // Actualiza el índice actual
    currentIndex += direction;

    // Asegúrate de que el índice esté dentro de los límites
    if (currentIndex < 0) {
        currentIndex = totalItems - 1;
    } else if (currentIndex >= totalItems) {
        currentIndex = 0;
    }

    // Mueve el carrusel
    const offset = -currentIndex * 33; // Cada imagen ocupa el 33% del ancho
    carousel.style.transform = `translateX(${offset}%)`;
}
// Funcionalidad para los acordeones
        const accordions = document.getElementsByClassName("accordion");
        for (let i = 0; i < accordions.length; i++) {
            accordions[i].addEventListener("click", function() {
                this.classList.toggle("active");
                const panel = this.nextElementSibling;
                if (panel.style.maxHeight) {
                    panel.style.maxHeight = null;
                } else {
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
            });
        }


