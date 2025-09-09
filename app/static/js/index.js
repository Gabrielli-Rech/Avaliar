        // Alternância de tema
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;
        const themeIcon = themeToggle.querySelector('i');

        // Verificar se há uma preferência salva
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            body.classList.add(savedTheme);
            updateThemeIcon();
        }

        // Alternar tema ao clicar no botão
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-theme');

            // Salvar preferência
            const currentTheme = body.classList.contains('light-theme') ? 'light-theme' : '';
            localStorage.setItem('theme', currentTheme);

            // Atualizar ícone
            updateThemeIcon();
        });

        // Atualizar ícone do tema
        function updateThemeIcon() {
            if (body.classList.contains('light-theme')) {
                themeIcon.className = 'fas fa-sun';
            } else {
                themeIcon.className = 'fas fa-moon';
            }
        }

        // Efeito de categoria ativa
        const categoryButtons = document.querySelectorAll('.category-btn');
        categoryButtons.forEach(button => {
            button.addEventListener('click', () => {
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
            });
        });
