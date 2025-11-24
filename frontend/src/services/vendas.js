import { request } from './config';

export default {
    async listar(inicio = null, fim = null, page = null, limit = null) {
        const params = new URLSearchParams();
        if (inicio) params.append('inicio', inicio);
        if (fim) params.append('fim', fim);
        if (page) params.append('page', page);
        if (limit) params.append('limit', limit);

        return request(`/dados?${params.toString()}`);
    },

    async criar(dados) {
        return request('/dados', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
    },

    async atualizar(id, dados) {
        return request(`/dados/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
    },

    async deletar(id) {
        return request(`/dados/${id}`, {
            method: 'DELETE'
        });
    }
}