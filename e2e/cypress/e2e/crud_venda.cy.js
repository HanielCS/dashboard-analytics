describe('Fluxo de Vendas', () => {
  
  const VENDA_TESTE = {
    data: '01/01',
    categoria: 'Jogos',
    valorInput: '999,99',
    valorParcial: '999,99' 
  }

  beforeEach(() => {
    cy.visit('/')
    cy.get('.spinner').should('not.exist')
    cy.get('.list-header').should('be.visible')
  })

  it('Deve criar, filtrar e deletar uma venda', () => {
    cy.contains('button', 'Todos').click()
    cy.wait(500)
    
    cy.get('body').then(($body) => {
      if ($body.find(`.list-item:contains("${VENDA_TESTE.valorParcial}")`).length > 0) {
        cy.log('Limpando dados antigos...')
        cy.get(`.list-item:contains("${VENDA_TESTE.valorParcial}")`).each(($el) => {
          cy.wrap($el).find('.delete-btn').click()
          cy.get('.btn-confirm').click()
          cy.wait(500)
        })
      }
    })

    // PASSO 1: CRIAR VENDA
    cy.log('Criando nova venda...')
    cy.get('input[placeholder="Data"]').clear().type(VENDA_TESTE.data)
    cy.get('select').select(VENDA_TESTE.categoria)
    cy.get('input[placeholder="Valor (R$)"]').clear().type(VENDA_TESTE.valorInput)
    cy.get('.qty-btn').contains('+').click().click() 
    cy.get('button').contains('Salvar').click()
    cy.contains('Venda registrada com sucesso!').should('be.visible')

    // PASSO 2: FILTRAR
    cy.contains('button', 'Todos').click()
    cy.wait(1000)

    // PASSO 3: VERIFICAR NA LISTA
    cy.get('.lista').contains(VENDA_TESTE.valorParcial).scrollIntoView().should('be.visible')

    // --- PASSO 4: DELETAR ---
    cy.get('.list-item')
      .filter(`:contains("${VENDA_TESTE.valorParcial}")`)
      .first()
      .within(() => {
        cy.get('.delete-btn').click()
      })
    cy.get('.modal-content').should('be.visible')
    cy.get('.btn-confirm').click()
    cy.contains('Venda removida').should('be.visible')
    cy.get('.lista').should('not.contain', VENDA_TESTE.valorParcial)
  })
})