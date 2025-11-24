import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import SaleForm from '../SaleForm.vue'
import api from '../../services/api'

// --- MOCK DA API ---
// Dizemos ao Vitest: "Não uses o api.js real, usa este falso aqui"
// Isto evita que o teste tente conectar ao Backend real
vi.mock('../../services/api', () => ({
  default: {
    criarVenda: vi.fn(() => Promise.resolve({ id: 1 })), // Simula sucesso
    atualizarVenda: vi.fn(() => Promise.resolve({ id: 1 }))
  }
}))

describe('SaleForm.vue', () => {
  
  beforeEach(() => {
    vi.clearAllMocks() // Limpa contadores antes de cada teste
  })

  it('impede envio com campos vazios', async () => {
    // Mock do window.alert (pois ele não existe no ambiente de teste JSDOM por padrão)
    window.alert = vi.fn()
    
    const wrapper = mount(SaleForm)
    
    // Tenta clicar em salvar sem preencher nada (vendas e qtd vazios)
    await wrapper.find('.save-btn').trigger('click')
    
    // Verifica se o alerta foi chamado
    expect(window.alert).toHaveBeenCalled()
    // Verifica se a API NÃO foi chamada (o teste passou se isso for verdade)
    expect(api.criarVenda).not.toHaveBeenCalled()
  })

  it('envia dados corretamente ao criar nova venda', async () => {
    const wrapper = mount(SaleForm)

    // 1. Preenche os campos
    // Encontra inputs. A ordem depende do seu template.
    // Assumindo: [0]=Data, [1]=Valor, [2]=Qtd (dentro do grupo personalizado)
    // Nota: O input de quantidade pode ser difícil de achar se estiver dentro da div .qty-input-group
    
    const inputValor = wrapper.findAll('input[type="number"]')[0] // Valor Total
    const inputQtd = wrapper.findAll('input[type="number"]')[1]   // Qtd
    const inputData = wrapper.find('input[placeholder="Data"]')

    await inputData.setValue('10/10')
    await inputValor.setValue(100)
    await inputQtd.setValue(5)

    // 2. Clica em Salvar
    await wrapper.find('.save-btn').trigger('click')

    // 3. Verifica se a API foi chamada com os dados certos
    expect(api.criarVenda).toHaveBeenCalledTimes(1)
    expect(api.criarVenda).toHaveBeenCalledWith(expect.objectContaining({
      data: '10/10',
      vendas: 100,
      qtd_pedidos: 5,
      categoria: 'Eletrônicos' // Valor padrão
    }))

    // 4. Verifica se o componente avisou o Pai (emit)
    // O 'venda-salva' é emitido após o sucesso da API
    // Como a API é assíncrona, precisamos esperar as promessas resolverem
    await new Promise(resolve => setTimeout(resolve, 0))
    expect(wrapper.emitted()).toHaveProperty('venda-salva')
  })

  it('entra em modo de edição quando recebe prop', async () => {
    const dadosEdicao = {
      id: 99,
      data: '25/12',
      categoria: 'Jogos',
      vendas: 500,
      qtd_pedidos: 1
    }

    const wrapper = mount(SaleForm, {
      props: {
        vendaParaEditar: dadosEdicao
      }
    })

    // Verifica se o texto do botão mudou para "Atualizar"
    expect(wrapper.find('.save-btn').text()).toContain('Atualizar')
    
    // Verifica se os inputs foram preenchidos automaticamente
    const inputValor = wrapper.findAll('input[type="number"]')[0]
    expect(inputValor.element.value).toBe('500')
    
    // Testa o envio da Edição
    await wrapper.find('.save-btn').trigger('click')
    
    // Deve chamar atualizarVenda, não criarVenda
    expect(api.atualizarVenda).toHaveBeenCalledTimes(1)
    expect(api.atualizarVenda).toHaveBeenCalledWith(99, expect.objectContaining({
      vendas: 500,
      categoria: 'Jogos'
    }))
  })
})