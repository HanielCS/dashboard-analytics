<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'
import toast from '../services/toast'

const props = defineProps({
  vendaParaEditar: Object
})

const emit = defineEmits(['venda-salva', 'cancelar-edicao'])

const form = ref({
  data: '',
  categoria: 'Eletrônicos',
  vendas: '', // String vazia inicial para permitir digitação livre
  qtd_pedidos: ''
})

const enviando = ref(false)
const modoEdicao = ref(false)

// --- Lógica de Estado ---
const getDataHoje = () => new Date().toLocaleDateString('pt-BR').slice(0, 5)

const resetarForm = () => {
  form.value = {
    data: getDataHoje(),
    categoria: 'Eletrônicos',
    vendas: '',
    qtd_pedidos: ''
  }
  modoEdicao.value = false
}

// Observa mudanças na prop para preencher o formulário na edição
watch(() => props.vendaParaEditar, (novaVenda) => {
  if (novaVenda) {
    form.value = { ...novaVenda }
    // Garante que o valor seja string para edição no input type="text"
    if (form.value.vendas) form.value.vendas = form.value.vendas.toString()
    modoEdicao.value = true
  } else {
    resetarForm()
  }
}, { immediate: true })

// --- Controle de Quantidade ---
const incrementarQtd = () => {
  const valor = Number(form.value.qtd_pedidos) || 0
  form.value.qtd_pedidos = valor + 1
}

const decrementarQtd = () => {
  const valor = Number(form.value.qtd_pedidos) || 0
  if (valor > 1) {
    form.value.qtd_pedidos = valor - 1
  }
}

// --- Ações ---
const salvar = async () => {
  if (!form.value.vendas && !form.value.qtd_pedidos) {
    return toast.warning("Por favor, preencha o valor e a quantidade.")
  }

  if (!form.value.vendas) {
    return toast.warning("Por favor, preencha o valor.") // <--- AQUI
  }

  if (!form.value.qtd_pedidos) {
    return toast.warning("Por favor, preencha a quantidade.") // <--- AQUI
  }

  enviando.value = true
  
  try {
    // Tratamento de Valor (Vírgula para Ponto)
    let valorString = form.value.vendas.toString()
    valorString = valorString.replace(',', '.')
    const valorFinal = parseFloat(valorString)

    if (isNaN(valorFinal)) {
      alert("Valor inválido!")
      enviando.value = false
      return
    }

    const payload = {
      ...form.value,
      vendas: valorFinal
    }

    if (modoEdicao.value) {
      await api.atualizarVenda(form.value.id, payload)
      emit('cancelar-edicao')
    } else {
      await api.criarVenda(payload)
    }
    
    emit('venda-salva')
    resetarForm()

    toast.success(modoEdicao.value ? "Venda atualizada!" : "Venda registrada com sucesso!") // <--- AQUI
    
  } catch (error) {
    console.error(error)
    toast.error("Ocorreu um erro ao salvar.") // <--- AQUI
  } finally {
    enviando.value = false
  }
}

const cancelar = () => {
  resetarForm()
  emit('cancelar-edicao')
}
</script>

<template>
  <div class="form-card card-base" :class="{ 'edit-mode': modoEdicao }">
    
    <h3 class="form-title">
      <span v-if="modoEdicao">✏️ EDITANDO VENDA</span>
      <span v-else>➕ REGISTRAR NOVA VENDA</span>
    </h3>
    
    <div class="form-body">
      
      <!-- LINHA 1: CAMPOS DE ENTRADA -->
      <div class="fields-row">
        <!-- Data -->
        <input 
          v-model="form.data" 
          placeholder="Data" 
          class="input-field input-small" 
        />
        
        <!-- Categoria -->
        <select v-model="form.categoria" class="input-field input-select">
          <option>Eletrônicos</option>
          <option>Roupas</option>
          <option>Casa</option>
          <option>Jogos</option>
          <option>Livros</option>
        </select>
        
        <!-- Valor (Texto para aceitar vírgula) -->
        <input 
          v-model="form.vendas" 
          type="text" 
          inputmode="decimal" 
          placeholder="Valor (R$)" 
          class="input-field"
        />

        <!-- Input Qtd com Botões -->
        <div class="qty-input-group">
          <button type="button" @click="decrementarQtd" class="qty-btn">-</button>
          <input 
            v-model.number="form.qtd_pedidos" 
            type="number" 
            placeholder="Qtd" 
            class="input-qty"
            min="1"
          />
          <button type="button" @click="incrementarQtd" class="qty-btn">+</button>
        </div>
      </div>
      
      <!-- LINHA 2: BOTÕES DE AÇÃO (EMBAIXO) -->
      <div class="actions-row">
        
        <!-- Botão Cancelar (Visível apenas na edição) -->
        <button 
          v-if="modoEdicao" 
          @click="cancelar" 
          class="btn-modern cancel-btn"
          title="Cancelar Edição"
        >
          <span class="icon-text">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            Cancelar
          </span>
        </button>

        <!-- Botão Salvar/Atualizar -->
        <button 
          @click="salvar" 
          :disabled="enviando" 
          class="btn-modern save-btn"
        >
          <span v-if="enviando" class="loader"></span>
          <span v-else class="icon-text">
            <!-- Ícone Salvar -->
            <svg v-if="!modoEdicao" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
            <!-- Ícone Atualizar -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
            {{ modoEdicao ? 'Atualizar Venda' : 'Salvar Venda' }}
          </span>
        </button>

      </div>

    </div>
  </div>
</template>

<style scoped src="../assets/styles/SaleForm.css"></style>