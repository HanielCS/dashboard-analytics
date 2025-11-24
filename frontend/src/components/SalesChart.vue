<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, 
  PointElement, LineElement, LineController // Importações para Linha
} from 'chart.js'

// Registra controladores para gráficos mistos (Barra + Linha)
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, LineController)

const props = defineProps({
  dados: { type: Array, required: true },
  predicoes: { type: Array, default: () => [] } // Recebe a predição
})

const chartData = computed(() => {
  // 1. Combina as datas reais com as futuras
  const labelsReais = props.dados.map(d => d.data)
  const labelsFuturas = props.predicoes.map(p => p.data)
  const labels = [...labelsReais, ...labelsFuturas]

  // 2. Dados Reais (Preenche com null nos dias futuros)
  const dataReais = props.dados.map(d => d.vendas)
  const paddingReais = new Array(labelsFuturas.length).fill(null)
  
  // 3. Dados Futuros (Preenche com null nos dias passados)
  const paddingFuturos = new Array(labelsReais.length).fill(null)
  // Dica: Adiciona o último valor real como ponto de partida para a linha conectar
  if (dataReais.length > 0) {
    paddingFuturos[paddingFuturos.length - 1] = dataReais[dataReais.length - 1]
  }
  const dataFuturos = props.predicoes.map(p => p.vendas)

  return {
    labels: labels,
    datasets: [
      {
        type: 'bar',
        label: 'Vendas Realizadas',
        data: [...dataReais, ...new Array(labelsFuturas.length).fill(null)],
        backgroundColor: '#3498db',
        borderRadius: 4,
        order: 1
      },
      {
        type: 'line',
        label: 'Tendência (IA)',
        // Ajuste para alinhar o array de predição com o final do array real
        data: [...new Array(labelsReais.length).fill(null), ...dataFuturos],
        borderColor: '#f39c12', // Laranja
        borderWidth: 2,
        borderDash: [5, 5], // Linha pontilhada
        pointRadius: 4,
        tension: 0.4, // Suavização da curva
        fill: false,
        order: 2
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: { position: 'bottom' },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) label += ': ';
          if (context.parsed.y !== null) {
            label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed.y);
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
    <h3 class="chart-title">Evolução e Tendência</h3>
    <div class="canvas-wrapper">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped src="../assets/styles/SalesChart.css"></style>