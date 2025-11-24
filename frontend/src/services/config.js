export const API_URL = '/api';

export async function request(endpoint, options = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, options);
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erro na requisição: ${response.status}`);
    }
    
    return response.json();
}