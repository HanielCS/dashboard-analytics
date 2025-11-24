<script setup>
const props = defineProps({
  totais: { type: Object, required: true },   // Objeto { vendas, pedidos, ticket }
  variacao: { type: Object, required: true }, // Objeto { vendas, pedidos, ticket }
  melhorCategoria: { type: String, default: '-' }
})

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor)
}

// Helper para decidir a cor e o ícone
const getBadgeInfo = (valor) => {
  if (valor > 0) return { class: 'badge-up', icon: '▲', text: `+${valor.toFixed(1)}%` }
  if (valor < 0) return { class: 'badge-down', icon: '▼', text: `${valor.toFixed(1)}%` }
  return { class: 'badge-neutral', icon: '-', text: '0%' }
}
</script>

<template>
  <div class="kpi-grid">
    
    <!-- Total Vendido -->
    <div class="kpi-card card-base">
      <h3>Total Vendido</h3>
      <div class="kpi-content">
        <p class="valor destaque-verde">{{ formatarMoeda(totais.vendas) }}</p>
        <span class="badge" :class="getBadgeInfo(variacao.vendas).class">
          {{ getBadgeInfo(variacao.vendas).icon }} {{ getBadgeInfo(variacao.vendas).text }}
        </span>
      </div>
    </div>

    <!-- Pedidos -->
    <div class="kpi-card card-base">
      <h3>Pedidos</h3>
      <div class="kpi-content">
        <p class="valor">{{ totais.pedidos }}</p>
        <span class="badge" :class="getBadgeInfo(variacao.pedidos).class">
          {{ getBadgeInfo(variacao.pedidos).icon }} {{ getBadgeInfo(variacao.pedidos).text }}
        </span>
      </div>
    </div>

    <!-- Ticket Médio -->
    <div class="kpi-card card-base">
      <h3>Ticket Médio</h3>
      <div class="kpi-content">
        <p class="valor destaque-azul">{{ formatarMoeda(totais.ticket) }}</p>
        <span class="badge" :class="getBadgeInfo(variacao.ticket).class">
          {{ getBadgeInfo(variacao.ticket).icon }} {{ getBadgeInfo(variacao.ticket).text }}
        </span>
      </div>
    </div>

    <!-- Top Categoria -->
    <div class="kpi-card card-base">
      <h3>Top Categoria</h3>
      <div class="kpi-content">
        <p class="valor destaque-roxo texto-longo">{{ melhorCategoria }}</p>
      </div>
    </div>

  </div>
</template>

<style scoped src="../assets/styles/KPIsCards.css"></style>