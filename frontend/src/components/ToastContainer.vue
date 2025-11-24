<script setup>
import { toastState } from '../services/toast'
import toastService from '../services/toast'
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div 
        v-for="toast in toastState.items" 
        :key="toast.id"
        class="toast-item"
        :class="toast.tipo"
        @click="toastService.remove(toast.id)"
      >
        <!-- Ícones baseados no tipo -->
        <span v-if="toast.tipo === 'success'" class="icon">✅</span>
        <span v-if="toast.tipo === 'error'" class="icon">❌</span>
        <span v-if="toast.tipo === 'info'" class="icon">ℹ️</span>
        <span v-if="toast.tipo === 'warning'" class="icon">⚠️</span>
        
        <span class="message">{{ toast.mensagem }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
/* Container fixo no canto superior direito */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none; /* Deixa clicar "através" do container vazio */
}

.toast-item {
  pointer-events: auto; /* Reativa clique no toast */
  min-width: 300px;
  padding: 15px 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-weight: 500;
  border-left: 5px solid #ddd;
  font-family: 'Segoe UI', sans-serif;
}

/* Cores por Tipo */
.success { border-left-color: var(--success-color); color: #2c3e50; }
.error { border-left-color: var(--danger-color); color: #c0392b; }
.info { border-left-color: var(--accent-color); color: #2980b9; }
.warning { border-left-color: var(--warning-color); color: #d35400; }

/* Animações de Entrada/Saída (TransitionGroup) */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>