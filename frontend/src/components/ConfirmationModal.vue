<script setup>
defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: 'Confirmação' },
  message: { type: String, default: 'Tem certeza que deseja realizar esta ação?' }
})

const emit = defineEmits(['confirm', 'cancel'])
</script>

<template>
  <!-- O Teleport joga o modal para o final do body, evitando problemas de z-index -->
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click="$emit('cancel')">
      
      <!-- O @click.stop impede que clicar no modal feche ele -->
      <div class="modal-content card-base" @click.stop>
        
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-btn" @click="$emit('cancel')">×</button>
        </div>

        <div class="modal-body">
          <p>{{ message }}</p>
        </div>

        <div class="modal-footer">
          <button class="btn-modal btn-cancel" @click="$emit('cancel')">Cancelar</button>
          <button class="btn-modal btn-confirm" @click="$emit('confirm')">Confirmar</button>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<style scoped src="../assets/styles/ConfirmationModal.css"></style>