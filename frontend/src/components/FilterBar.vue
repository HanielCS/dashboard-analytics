<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['filtrar'])

// Datas do formulário
const datas = ref({
  inicio: '',
  fim: ''
})

// Botão ativo para estilização
const filtroAtivo = ref('todos')

// Funções auxiliares de data
const hoje = new Date()
const formatarDataISO = (date) => date.toISOString().split('T')[0]

const aplicarFiltro = (tipo) => {
  filtroAtivo.value = tipo
  let inicio, fim

  if (tipo === '7dias') {
    const d = new Date()
    d.setDate(d.getDate() - 7)
    inicio = formatarDataISO(d)
    fim = formatarDataISO(hoje)
  } 
  else if (tipo === 'mes') {
    const d = new Date(hoje.getFullYear(), hoje.getMonth(), 1)
    inicio = formatarDataISO(d)
    fim = formatarDataISO(hoje)
  } 
  else if (tipo === 'todos') {
    inicio = null
    fim = null
  }
  else if (tipo === 'personalizado') {
    inicio = datas.value.inicio
    fim = datas.value.fim
  }

  // Atualiza os inputs visuais se for um botão rápido
  if (inicio && fim) {
    datas.value.inicio = inicio
    datas.value.fim = fim
  }

  // Emite para o App.vue buscar os dados
  emit('filtrar', { inicio, fim })
}

onMounted(() => {
  // Define datas iniciais nos inputs apenas visualmente
  const d = new Date()
  d.setDate(d.getDate() - 30)
  datas.value.inicio = formatarDataISO(d)
  datas.value.fim = formatarDataISO(hoje)
})
</script>

<template>
  <div class="filter-bar card-base">
    <div class="quick-actions">
      <span class="label">Filtrar por:</span>
      <button 
        @click="aplicarFiltro('todos')" 
        class="filter-btn" 
        :class="{ active: filtroAtivo === 'todos' }"
      >Todos</button>
      
      <button 
        @click="aplicarFiltro('7dias')" 
        class="filter-btn" 
        :class="{ active: filtroAtivo === '7dias' }"
      >7 Dias</button>
      
      <button 
        @click="aplicarFiltro('mes')" 
        class="filter-btn" 
        :class="{ active: filtroAtivo === 'mes' }"
      >Este Mês</button>
    </div>

    <div class="custom-range">
      <input type="date" v-model="datas.inicio" />
      <span class="separator">até</span>
      <input type="date" v-model="datas.fim" />
      <button @click="aplicarFiltro('personalizado')" class="btn-go">Ir</button>
    </div>
  </div>
</template>

<style scoped src="../assets/styles/FilterBar.css"></style>