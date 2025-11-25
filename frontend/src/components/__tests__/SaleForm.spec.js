import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SaleForm from '../SaleForm.vue'
import api from '../../services/api'
import toast from '../../services/toast' // Importamos o serviço de toast real

// MOCKS
// Simulação a API para não fazer chamadas reais ao Backend durante o teste
vi.mock('../../services/api', () => ({
  default: {
    criarVenda: vi.fn(() => Promise.resolve({ id: 1 })),
    atualizarVenda: vi.fn(() => Promise.resolve({ id: 1 }))
  }
}))

// Simulação do Toast para verificar se ele foi chamado, sem precisar renderizar na tela
vi.mock('../../services/toast', () => ({
  default: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn()
  }
}))

describe('SaleForm.vue', () => {
  
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('impede envio com campos vazios', async () => {
    const wrapper = mount(SaleForm)
    
    // Tenta clicar em salvar sem preencher nada
    await wrapper.find('.save-btn').trigger('click')
    
    // Verifica se o TOAST de aviso foi chamado
    expect(toast.warning).toHaveBeenCalled()
    
    // Verifica se a API NÃO foi chamada
    expect(api.criarVenda).not.toHaveBeenCalled()
  })

  it('envia dados corretamente ao criar nova venda', async () => {
    const wrapper = mount(SaleForm)

    // 1. Preenche os campos
    const inputData = wrapper.find('input[placeholder="Data"]')
    const inputValor = wrapper.find('input[placeholder="Valor (R$)"]') // type="text"
    const inputQtd = wrapper.find('input[placeholder="Qtd"]')

    await inputData.setValue('10/10')
    await inputValor.setValue('100,50') // Testando com vírgula para verificar a conversão
    await inputQtd.setValue(5)

    // 2. Clica em Salvar
    await wrapper.find('.save-btn').trigger('click')

    // 3. Verifica se a API foi chamada com os dados certos e convertidos
    expect(api.criarVenda).toHaveBeenCalledTimes(1)
    
    expect(api.criarVenda).toHaveBeenCalledWith(expect.objectContaining({
      data: '10/10',
      vendas: 100.50,
      qtd_pedidos: 5,
      categoria: 'Eletrônicos'
    }))

    // 4. Aguarda o ciclo de promessa para verificar o sucesso
    await new Promise(resolve => setTimeout(resolve, 0))
    expect(toast.success).toHaveBeenCalled()
    
    expect(wrapper.emitted()).toHaveProperty('venda-salva')
  })

  it('entra em modo de edição quando recebe prop', async () => {
    const dadosEdicao = {
      id: 99,
      data: '25/12',
      categoria: 'Jogos',
      vendas: 500.00,
      qtd_pedidos: 1
    }

    const wrapper = mount(SaleForm, {
      props: {
        vendaParaEditar: dadosEdicao
      }
    })

    // Verifica se o texto do botão mudou para "Atualizar"
    expect(wrapper.find('.save-btn').text()).toContain('Atualizar')
    
    // Verifica se o input de valor foi preenchido corretamente (convertido para string no formulário)
    const inputValor = wrapper.find('input[placeholder="Valor (R$)"]')
    expect(inputValor.element.value).toBe('500')
    
    // Simula o clique em Atualizar
    await wrapper.find('.save-btn').trigger('click')
    
    // Verifica se chamou a rota de atualização (PUT) em vez de criação
    expect(api.atualizarVenda).toHaveBeenCalledTimes(1)
    expect(api.atualizarVenda).toHaveBeenCalledWith(99, expect.objectContaining({
      vendas: 500,
      categoria: 'Jogos'
    }))
  })
})