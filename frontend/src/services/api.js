import vendasService from './vendas';
import kpiService from './kpi';
import predicaoService from './predicao';
import arquivosService from './arquivos';

// Mantém a compatibilidade com o código existente
export default {
    // Vendas (CRUD)
    getVendas: vendasService.listar,
    criarVenda: vendasService.criar,
    atualizarVenda: vendasService.atualizar,
    deletarVenda: vendasService.deletar,

    // KPIs (Business Intelligence)
    getKPIs: kpiService.buscar,

    // Predição (IA)
    getPredicao: predicaoService.gerar,

    // Arquivos (Importação e Exportação)
    downloadArquivo: arquivosService.download,
    importarCSV: arquivosService.importarCSV
};