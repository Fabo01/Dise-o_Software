class UIComponents {
    constructor() {
        // Inicialización si es necesaria
    }
    
    showModal(title, content) {
        document.getElementById('modal-body').innerHTML = `
            <h2>${title}</h2>
            ${content}
        `;
        document.getElementById('modal-container').style.display = 'block';
    }
    
    hideModal() {
        document.getElementById('modal-container').style.display = 'none';
    }
    
    showAlert(message, type = 'success') {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;
        
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
    
    showConfirm(message, callback) {
        const confirmHtml = `
            <div class="confirm-dialog">
                <p>${message}</p>
                <div class="confirm-buttons">
                    <button id="confirm-yes" class="btn btn-danger">Sí</button>
                    <button id="confirm-no" class="btn">No</button>
                </div>
            </div>
        `;
        
        this.showModal('Confirmar', confirmHtml);
        
        document.getElementById('confirm-yes').addEventListener('click', () => {
            callback();
            this.hideModal();
        });
        
        document.getElementById('confirm-no').addEventListener('click', () => {
            this.hideModal();
        });
    }
    
    // Otros métodos de utilidad para UI...
}