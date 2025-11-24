<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  ArcElement 
} from 'chart.js'

// Registra o elemento "Arc" necessário para gráficos redondos
ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps({
  dados: { type: Array, required: true }
})

// --- Lógica: Agrupar vendas por categoria ---
const chartData = computed(() => {
  // 1. Cria um objeto acumulador: { "Eletrônicos": 500, "Casa": 200 }
  const agrupado = props.dados.reduce((acc, item) => {
    if (!acc[item.categoria]) acc[item.categoria] = 0
    acc[item.categoria] += item.vendas
    return acc
  }, {})

  // 2. Separa labels e valores para o Chart.js
  return {
    labels: Object.keys(agrupado),
    datasets: [{
      data: Object.values(agrupado),
      backgroundColor: [
        '#3498db', // Azul
        '#e74c3c', // Vermelho
        '#f1c40f', // Amarelo
        '#2ecc71', // Verde
        '#9b59b6', // Roxo
        '#34495e'  // Cinza Escuro
      ],
      hoverOffset: 4
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'right' }, // Legenda ao lado fica mais elegante
    tooltip: {
      callbacks: {
        label: function(context) {
          // Formata tooltip para R$
          let label = context.label || '';
          if (label) label += ': ';
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed);
          }
          return label;
        }
      }
    }
  }
}
</script>

<template>
  <div class="chart-container card-base">
    <h3 class="chart-title">Vendas por Categoria</h3>
    <div class="canvas-wrapper">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped src="../assets/styles/CategoryChart.css"></style>