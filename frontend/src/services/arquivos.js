import { API_URL, request } from './config';

export default {
    download(tipo, inicio, fim) {
        const url = `${API_URL}/export/${tipo}?inicio=${inicio}&fim=${fim}`;
        window.open(url, '_blank');
    },

    async importarCSV(arquivo) {
        const formData = new FormData();
        formData.append('file', arquivo);

        return request('/import/csv', {
            method: 'POST',
            body: formData
        });
    }
}