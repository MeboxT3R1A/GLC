// Sistema de Gerenciamento de Clube de Desbravadores - JavaScript Customizado

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Máscara para telefone
    const telefoneInputs = document.querySelectorAll('input[type="tel"]');
    telefoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
            value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            e.target.value = value;
        });
    });

    // Máscara para CPF
    const cpfInputs = document.querySelectorAll('input[data-mask="cpf"]');
    cpfInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/^(\d{3})(\d)/g, '$1.$2');
            value = value.replace(/^(\d{3})\.(\d{3})(\d)/g, '$1.$2.$3');
            value = value.replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/g, '$1.$2.$3-$4');
            e.target.value = value;
        });
    });

    // Máscara para CEP
    const cepInputs = document.querySelectorAll('input[data-mask="cep"]');
    cepInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/^(\d{5})(\d)/g, '$1-$2');
            e.target.value = value;
        });
    });

    // Máscara para moeda
    const currencyInputs = document.querySelectorAll('input[data-mask="currency"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value / 100).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
            e.target.value = value;
        });
    });

    // Confirmação antes de deletar/inativar
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Tem certeza que deseja realizar esta ação?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-save para formulários longos
    const forms = document.querySelectorAll('form[data-autosave]');
    forms.forEach(function(form) {
        const formId = form.getAttribute('data-autosave');
        
        // Salvar dados no localStorage quando o usuário digita
        form.addEventListener('input', function() {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem('form_' + formId, JSON.stringify(data));
        });

        // Restaurar dados salvos quando a página carrega
        const savedData = localStorage.getItem('form_' + formId);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(function(key) {
                const input = form.querySelector('[name="' + key + '"]');
                if (input && input.type !== 'password') {
                    input.value = data[key];
                }
            });
        }

        // Limpar dados salvos quando o formulário é enviado
        form.addEventListener('submit', function() {
            localStorage.removeItem('form_' + formId);
        });
    });

    // Busca em tempo real
    const searchInputs = document.querySelectorAll('input[data-search]');
    searchInputs.forEach(function(input) {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Implementar busca AJAX aqui se necessário
                console.log('Buscando:', input.value);
            }, 300);
        });
    });

    // Validação de formulários
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Animações de entrada
    const animatedElements = document.querySelectorAll('.fade-in');
    animatedElements.forEach(function(element, index) {
        setTimeout(function() {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Contador de caracteres para textareas
    const textareas = document.querySelectorAll('textarea[data-maxlength]');
    textareas.forEach(function(textarea) {
        const maxLength = parseInt(textarea.getAttribute('data-maxlength'));
        const counter = document.createElement('small');
        counter.className = 'text-muted';
        counter.style.float = 'right';
        textarea.parentNode.appendChild(counter);

        function updateCounter() {
            const remaining = maxLength - textarea.value.length;
            counter.textContent = remaining + ' caracteres restantes';
            counter.className = remaining < 0 ? 'text-danger' : 'text-muted';
        }

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });

    // Ordenação de tabelas
    const sortableTables = document.querySelectorAll('table[data-sortable]');
    sortableTables.forEach(function(table) {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(function(header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                const column = this.getAttribute('data-sort');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                const isAscending = this.classList.contains('sort-asc');
                
                // Remover classes de ordenação de todos os headers
                headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
                
                // Adicionar classe ao header atual
                this.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
                
                // Ordenar linhas
                rows.sort(function(a, b) {
                    const aVal = a.querySelector('td[data-sort="' + column + '"]').textContent.trim();
                    const bVal = b.querySelector('td[data-sort="' + column + '"]').textContent.trim();
                    
                    if (isAscending) {
                        return bVal.localeCompare(aVal);
                    } else {
                        return aVal.localeCompare(bVal);
                    }
                });
                
                // Reordenar linhas na tabela
                rows.forEach(function(row) {
                    tbody.appendChild(row);
                });
            });
        });
    });

    // Notificações toast
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-' + type + ' border-0';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remover toast após ser escondido
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    }

    // Expor função globalmente
    window.showToast = showToast;

    // Atalhos de teclado
    document.addEventListener('keydown', function(e) {
        // Ctrl + S para salvar formulário
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            const form = document.querySelector('form');
            if (form) {
                form.submit();
            }
        }
        
        // Escape para fechar modais
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Lazy loading para imagens
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(function(img) {
        imageObserver.observe(img);
    });

    // Debounce para funções que são chamadas frequentemente
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = function() {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Throttle para funções que precisam ser limitadas
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Expor funções utilitárias globalmente
    window.debounce = debounce;
    window.throttle = throttle;

    console.log('Sistema de Desbravadores carregado com sucesso!');
});
