import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KPICards from '../KPICards.vue'

describe('KPICards.vue', () => {
  
  it('renderiza corretamente os valores das props', () => {
    // 1. Monta o componente com dados falsos
    const wrapper = mount(KPICards, {
      props: {
        totalVendas: 5000,
        totalPedidos: 50,
        melhorCategoria: 'Eletrônicos'
      }
    })

    // 2. Verifica se o texto renderizado contém os valores esperados
    // Nota: O espaço nbsp (não quebrável) às vezes é usado por formatadores, 
    // mas aqui esperamos o padrão "R$ 5.000,00"
    expect(wrapper.text()).toContain('R$ 5.000,00') // Verifica formatação de moeda
    expect(wrapper.text()).toContain('50')           // Verifica número de pedidos
    expect(wrapper.text()).toContain('Eletrônicos')  // Verifica categoria
  })

  it('calcula o ticket médio corretamente', () => {
    // Cenário: 1000 reais em 4 pedidos = média de 250
    const wrapper = mount(KPICards, {
      props: {
        totalVendas: 1000,
        totalPedidos: 4,
        melhorCategoria: 'Casa'
      }
    })

    // Verifica se o cálculo (1000 / 4 = 250) foi feito e formatado
    expect(wrapper.text()).toContain('R$ 250,00')
  })

  it('lida com zero pedidos para evitar divisão por zero', () => {
    const wrapper = mount(KPICards, {
      props: {
        totalVendas: 0,
        totalPedidos: 0
      }
    })

    // Se pedidos for 0, o ticket médio deve ser R$ 0,00 (não NaN ou Infinity)
    expect(wrapper.text()).toContain('R$ 0,00')
  })
})