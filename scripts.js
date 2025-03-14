function scrollToSection(id) {
  document.getElementById(id).scrollIntoView({ behavior: "smooth" });
}

function toggleSection(id) {
  const section = document.getElementById(id);
  section.classList.toggle("hidden-section");
}


