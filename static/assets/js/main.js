document.addEventListener("DOMContentLoaded", function() {

    // --- 1. CARREGAMENTO DINÂMICO DO HEADER ---
    // Esta função carrega o _header.html e o insere nas páginas.
    // Os scripts do menu e do scroll SÓ rodam DEPOIS que o header é carregado.
    const loadHeader = () => {
        const headerPlaceholder = document.getElementById("header-placeholder");
        // Roda apenas se o placeholder do header existir na página
        if (headerPlaceholder) {
            fetch('_header.html')
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Arquivo _header.html não encontrado.");
                    }
                    return response.text();
                })
                .then(data => {
                    headerPlaceholder.innerHTML = data;

                    // --- FUNÇÕES QUE DEPENDEM DO HEADER CARREGADO ---

                    // A. Efeito de scroll que muda a cor do header
                    const header = document.querySelector('.main-header');
                    if (header) {
                        window.addEventListener('scroll', () => {
                            if (window.scrollY > 50) {
                                header.classList.add('scrolled');
                            } else {
                                header.classList.remove('scrolled');
                            }
                        });
                    }

                    // B. Funcionalidade do Menu Hamburger para mobile
                    const hamburger = document.querySelector('.hamburger-menu');
                    const nav = document.querySelector('.main-nav');
                    if (hamburger && nav) {
                        hamburger.addEventListener('click', () => {
                            nav.classList.toggle('active');
                        });
                    }
                })
                .catch(error => {
                    console.error('Erro ao carregar o header:', error);
                });
        }
    };

    // --- 2. FUNCIONALIDADE DO ACORDEÃO (Para Sorteios e FAQ) ---
    // Este código funciona de forma independente do header.
    const accordionItems = document.querySelectorAll('.accordion-item');
    if (accordionItems.length > 0) {
        accordionItems.forEach(item => {
            const accordionHeader = item.querySelector('.accordion-header');
            if (accordionHeader) {
                accordionHeader.addEventListener('click', () => {
                    item.classList.toggle('active');
                    const content = item.querySelector('.accordion-content');
                    if (content.style.maxHeight) {
                        content.style.maxHeight = null;
                    } else {
                        content.style.maxHeight = content.scrollHeight + "px";
                    }
                });
            }
        });
    }

    // --- 3. FUNCIONALIDADE DA LISTA DE PRODUTOS (Página Como Participar) ---
    const toggleProdutosBtn = document.querySelector('.toggle-produtos-btn');
    if (toggleProdutosBtn) {
        toggleProdutosBtn.addEventListener('click', () => {
            const listaProdutos = document.querySelector('#lista-de-produtos');
            toggleProdutosBtn.classList.toggle('active');
            
            const icon = toggleProdutosBtn.querySelector('.toggle-icon');
            const isExpanded = toggleProdutosBtn.getAttribute('aria-expanded') === 'true';

            if (isExpanded) {
                toggleProdutosBtn.setAttribute('aria-expanded', 'false');
                if (icon) icon.textContent = '+';
            } else {
                toggleProdutosBtn.setAttribute('aria-expanded', 'true');
                if (icon) icon.textContent = '–';
            }

            if (listaProdutos.style.maxHeight) {
                listaProdutos.style.maxHeight = null;
            } else {
                listaProdutos.style.maxHeight = listaProdutos.scrollHeight + "px";
            }
        });
    }

    // --- CHAMADA INICIAL PARA CARREGAR O HEADER ---
    loadHeader();

});

