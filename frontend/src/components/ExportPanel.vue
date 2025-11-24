<script setup>
import { ref } from 'vue'
import api from '../services/api'
import toast from '../services/toast' // Se você já tiver o toast, use. Se não, use alert.

// ... (código de datas anterior) ...
const hoje = new Date()
const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1)
const formatarISO = (date) => date.toISOString().split('T')[0]
const datas = ref({ inicio: formatarISO(inicioMes), fim: formatarISO(hoje) })

// Referência para o input invisível
const fileInput = ref(null)

const baixar = (tipo) => {
  if(!datas.value.inicio || !datas.value.fim) return alert("Selecione as datas")
  api.downloadArquivo(tipo, datas.value.inicio, datas.value.fim)
}

// Função chamada ao clicar no botão "Importar"
const abrirSeletor = () => {
  fileInput.value.click()
}

// Função chamada quando o usuário escolhe o arquivo
const processarArquivo = async (event) => {
  const arquivo = event.target.files[0]
  if (!arquivo) return

  try {
    toast.info("Enviando arquivo...")
    const res = await api.importarCSV(arquivo)
    
    if (res.erro) {
      toast.error(res.erro)
    } else {
      toast.info("Upload iniciado! Você será notificado quando terminar.")
      // Como é assíncrono, não adianta dar reload agora. 
      // Num sistema real, usaríamos WebSocket para avisar o fim.
      // Por enquanto, vamos dar um reload longo (5s) só para simular.
      setTimeout(() => location.reload(), 5000)
    }
  } catch (error) {
    toast.error("Erro ao enviar arquivo.")
  } finally {
    // Limpa o input para permitir selecionar o mesmo arquivo de novo se quiser
    event.target.value = ''
  }
}
</script>

<template>
  <div class="export-card card-base">
    <h3>
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f1c40f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="fill: #f1c40f; stroke: none;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
      Gestão de Arquivos
    </h3>
    
    <div class="panel-content">
      <!-- Input de Arquivo (Invisível) -->
      <input 
        type="file" 
        ref="fileInput" 
        accept=".csv" 
        style="display: none" 
        @change="processarArquivo"
      />

      <div class="dates-row">
        <div class="input-group">
          <label>De:</label>
          <input type="date" v-model="datas.inicio" />
        </div>
        <div class="input-group">
          <label>Até:</label>
          <input type="date" v-model="datas.fim" />
        </div>
      </div>

      <div class="buttons-row">
        <!-- Botão de Importar (NOVO) -->
        <button @click="abrirSeletor" class="btn-export import">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          Importar CSV
        </button>

        <!-- Botões de Exportar -->
        <button @click="baixar('pdf')" class="btn-export pdf">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          PDF
        </button>
        <button @click="baixar('excel')" class="btn-export excel">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="8" y1="21" x2="8" y2="13"></line><line x1="16" y1="21" x2="16" y2="9"></line><line x1="12" y1="21" x2="12" y2="15"></line></svg>
          Excel
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped src="../assets/styles/ExportPanel.css"></style>