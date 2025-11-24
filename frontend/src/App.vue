<script setup>
import { ref, onMounted, computed } from 'vue'
import api from './services/api'

// Componentes
import SaleForm from './components/SaleForm.vue'
import KPICards from './components/KPICards.vue'
import SalesChart from './components/SalesChart.vue'
import CategoryChart from './components/CategoryChart.vue'
import SalesList from './components/SalesList.vue'
import FilterBar from './components/FilterBar.vue'
import ExportPanel from './components/ExportPanel.vue'
import ToastContainer from './components/ToastContainer.vue'

// Estado
const dadosGraficos = ref([]) 
const dadosLista = ref([])    
const predicoes = ref([])     
const kpis = ref({ 
  totais: { vendas: 0, pedidos: 0, ticket: 0 }, 
  variacao: { vendas: 0, pedidos: 0, ticket: 0 } 
}) 
const paginacao = ref({ current_page: 1, pages: 1, total: 0 })

const itemParaEditar = ref(null)
const carregando = ref(false)
const erro = ref(null)

const filtroAtual = ref({ inicio: null, fim: null })
const paginaAtual = ref(1)
const ITENS_POR_PAGINA = 5 

// Funções de Carga
const carregarDados = async (filtros = null) => {
  carregando.value = true
  erro.value = null
  
  if (filtros) {
    filtroAtual.value = filtros
    paginaAtual.value = 1
  }

  try {
    const [graficosRes, listaRes, predicoesRes, kpisRes] = await Promise.all([
      api.getVendas(filtroAtual.value.inicio, filtroAtual.value.fim), 
      api.getVendas(filtroAtual.value.inicio, filtroAtual.value.fim, paginaAtual.value, ITENS_POR_PAGINA),
      api.getPredicao(),
      api.getKPIs(filtroAtual.value.inicio, filtroAtual.value.fim)
    ])
    
    dadosGraficos.value = graficosRes
    predicoes.value = predicoesRes
    dadosLista.value = listaRes.data
    kpis.value = kpisRes
    paginacao.value = {
      current_page: listaRes.current_page,
      pages: listaRes.pages,
      total: listaRes.total
    }
    
  } catch (e) {
    console.error(e)
    erro.value = "Erro ao conectar com o servidor."
  } finally {
    carregando.value = false
  }
}

const mudarPagina = async (novaPagina) => {
  paginaAtual.value = novaPagina
  try {
    const listaRes = await api.getVendas(
      filtroAtual.value.inicio, 
      filtroAtual.value.fim, 
      novaPagina, 
      ITENS_POR_PAGINA
    )
    dadosLista.value = listaRes.data
    paginacao.value = {
      current_page: listaRes.current_page,
      pages: listaRes.pages,
      total: listaRes.total
    }
  } catch (e) {
    alert("Erro ao mudar de página")
  }
}

const prepararEdicao = (item) => {
  itemParaEditar.value = item
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const limparEdicao = () => { itemParaEditar.value = null }

// Cálculos
const melhorCategoria = computed(() => {
  if (dadosGraficos.value.length === 0) return '-'
  const porCategoria = dadosGraficos.value.reduce((acc, item) => {
    acc[item.categoria] = (acc[item.categoria] || 0) + item.vendas
    return acc
  }, {})
  return Object.keys(porCategoria).reduce((a, b) => porCategoria[a] > porCategoria[b] ? a : b)
})

onMounted(() => carregarDados())
</script>

<template>
  <div class="dashboard-container">
    
    <ToastContainer />

    <div class="layout-grid">
      
      <!-- COLUNA ESQUERDA (MAIN) -->
      <main class="content">
        <header>
          <h1>📊 Dashboard Executivo</h1>
          <button @click="carregarDados()" :disabled="carregando" class="refresh-btn" title="Atualizar">
            <span v-if="carregando" class="loader-spin"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2c3e50" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display: block;"><path d="M23 4v6h-6"></path><path d="M1 20v-6h6"></path><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
          </button>
        </header>

        <div v-if="erro" class="error-banner">{{ erro }}</div>

        <div v-if="carregando && !dadosGraficos.length" class="loading-state">
          <div class="spinner"></div>
          <p>Carregando dados...</p>
        </div>

        <div v-else>
          <SaleForm 
            :vendaParaEditar="itemParaEditar" 
            @venda-salva="carregarDados" 
            @cancelar-edicao="limparEdicao" 
          />

          <div v-if="dadosGraficos.length > 0">
            <KPICards 
              :totais="kpis.totais" 
              :variacao="kpis.variacao" 
              :melhorCategoria="melhorCategoria" 
            />

            <div class="main-chart-wrapper">
              <SalesChart :dados="dadosGraficos" :predicoes="predicoes" />
            </div>

            <SalesList 
              :lista="dadosLista" 
              :paginacao="paginacao"
              @atualizar-lista="carregarDados" 
              @editar="prepararEdicao" 
              @mudar-pagina="mudarPagina"
            />
          </div>

          <div v-else class="empty-state">
            <p>📭 Nenhuma venda registrada no período.</p>
          </div>
        </div>
      </main>

      <!-- COLUNA DIREITA (SIDEBAR) -->
      <aside class="sidebar">
        <div class="sidebar-block">
          <FilterBar @filtrar="carregarDados" />
        </div>

        <div class="sidebar-block" v-if="dadosGraficos.length > 0">
          <ExportPanel />
        </div>

        <div class="sidebar-block" v-if="dadosGraficos.length > 0">
          <CategoryChart :dados="dadosGraficos" />
        </div>
      </aside>

    </div>
  </div>
</template>

<style scoped src="./assets/styles/App.css"></style>