import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import KPICards from '../KPICards.vue'

describe('KPICards.vue', () => {
  
  it('renderiza corretamente os valores das props', () => {
    const wrapper = mount(KPICards, {
      props: {
        totais: {
          vendas: 5000,
          pedidos: 50,
          ticket: 100
        },
        variacao: {
          vendas: 10,
          pedidos: 5,
          ticket: 2
        },
        melhorCategoria: 'Eletrônicos'
      }
    })

    // Verifica se o texto renderizado contém os valores formatados
    expect(wrapper.text()).toContain('5.000,00')    // Valor formatado
    expect(wrapper.text()).toContain('50')          // Pedidos
    expect(wrapper.text()).toContain('Eletrônicos') // Melhor Categoria
    expect(wrapper.text()).toContain('+10.0%')      // Variação (Badge)
  })

  it('renderiza badges de variação negativa corretamente', () => {
    const wrapper = mount(KPICards, {
      props: {
        totais: { vendas: 1000, pedidos: 10, ticket: 100 },
        variacao: { vendas: -5, pedidos: 0, ticket: 0 }
      }
    })

    expect(wrapper.text()).toContain('-5.0%')
  })
})