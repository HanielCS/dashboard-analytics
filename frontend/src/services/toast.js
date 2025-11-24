import { reactive } from 'vue'

// Estado reativo compartilhado por toda a app
export const toastState = reactive({
  items: []
})

let idCounter = 0

export default {
  // Adiciona uma notificação
  // tipo: 'success' | 'error' | 'info' | 'warning'
  show(tipo, mensagem, duracao = 3000) {
    const id = idCounter++
    
    const toast = {
      id,
      tipo,
      mensagem
    }
    
    toastState.items.push(toast)

    // Remove automaticamente após X segundos
    setTimeout(() => {
      this.remove(id)
    }, duracao)
  },

  success(msg) { this.show('success', msg) },
  error(msg) { this.show('error', msg) },
  info(msg) { this.show('info', msg) },
  warning(msg) { this.show('warning', msg) },

  remove(id) {
    const index = toastState.items.findIndex(t => t.id === id)
    if (index > -1) {
      toastState.items.splice(index, 1)
    }
  }
}