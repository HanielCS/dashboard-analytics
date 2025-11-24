<script setup>
import { ref } from 'vue'
import api from '../services/api'
import ConfirmationModal from './ConfirmationModal.vue' // <--- Importação
import toast from '../services/toast'

const props = defineProps({
  lista: { type: Array, required: true },
  paginacao: { type: Object, default: () => ({ current_page: 1, pages: 1, total: 0 }) }
})

const emit = defineEmits(['atualizar-lista', 'editar', 'mudar-pagina'])

// --- Lógica do Modal ---
const showModal = ref(false)
const idToDelete = ref(null)

// Ao clicar no botão de lixeira, apenas abre o modal e salva o ID
const confirmarExclusao = (id) => {
  idToDelete.value = id
  showModal.value = true
}

// Ação real de exclusão (chamada pelo botão "Confirmar" do modal)
const executarExclusao = async () => {
  showModal.value = false // Fecha o modal primeiro
  
  if (idToDelete.value) {
    try {
      await api.deletarVenda(idToDelete.value)
      emit('atualizar-lista')
      toast.success("Venda removida.") // <--- AQUI
    } catch (e) {
      toast.error("Não foi possível remover a venda.") // <--- AQUI
    }
  }
  idToDelete.value = null
}

const cancelarExclusao = () => {
  showModal.value = false
  idToDelete.value = null
}

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor)
}
</script>

<template>
  <div class="list-header">
    <h3 class="list-title">Histórico Recente</h3>
    <span class="page-info" v-if="paginacao.total > 0">
      Pág {{ paginacao.current_page }} de {{ paginacao.pages }}
    </span>
  </div>
  
  <div class="lista">
    <div v-for="item in lista" :key="item.id" class="list-item card-base">
      <div class="date-badge">{{ item.data }}</div>
      
      <div class="info">
        <strong>{{ item.categoria }}</strong>
        <small>{{ item.qtd_pedidos }} pedidos</small>
      </div>
      
      <div class="price">{{ formatarMoeda(item.vendas) }}</div>
      
      <div class="actions">
        <button @click="$emit('editar', item)" class="action-btn edit-btn" title="Editar">
          <svg style="display: block; width: 20px; height: 20px;" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f39c12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>
        </button>
        
        <!-- Mudamos @click para confirmarExclusao -->
        <button @click="confirmarExclusao(item.id)" class="action-btn delete-btn" title="Excluir">
          <svg style="display: block; width: 20px; height: 20px;" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e74c3c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
        </button>
      </div>
    </div>

    <div class="pagination-controls" v-if="paginacao.pages > 1">
      <button 
        @click="$emit('mudar-pagina', paginacao.current_page - 1)" 
        :disabled="paginacao.current_page === 1"
        class="page-btn"
      >◀ Anterior</button>
      
      <button 
        @click="$emit('mudar-pagina', paginacao.current_page + 1)" 
        :disabled="paginacao.current_page === paginacao.pages"
        class="page-btn"
      >Próxima ▶</button>
    </div>
  </div>

  <!-- O Componente Modal fica aqui, invisível até ser chamado -->
  <ConfirmationModal 
    :visible="showModal" 
    title="Excluir Venda" 
    message="Tem certeza que deseja remover este registro permanentemente? Esta ação não pode ser desfeita."
    @confirm="executarExclusao" 
    @cancel="cancelarExclusao" 
  />
</template>

<style scoped src="../assets/styles/SalesList.css"></style>