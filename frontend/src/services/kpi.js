import { request } from './config';

export default {
    async buscar(inicio = null, fim = null) {
        const params = new URLSearchParams();
        if (inicio) params.append('inicio', inicio);
        if (fim) params.append('fim', fim);
        
        return request(`/kpis?${params.toString()}`);
    }
}