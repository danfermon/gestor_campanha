document.querySelectorAll('.accordion-header').forEach((btn) => {
  btn.addEventListener('click', () => {
    const content = btn.nextElementSibling;
    const isActive = content.classList.contains('active');

    // Fecha todos os outros
    document.querySelectorAll('.accordion-content').forEach((el) => el.classList.remove('active'));
    document.querySelectorAll('.accordion-header').forEach((el) => {
      el.classList.remove('active');
      el.querySelector('.arrow').textContent = '▶';
    });

    // Ativa o clicado, se ainda não estava ativo
    if (!isActive) {
      content.classList.add('active');
      btn.classList.add('active');
      btn.querySelector('.arrow').textContent = '▼';
    }
  });
});
