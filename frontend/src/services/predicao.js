import { request } from './config';

export default {
    async gerar() {
        return request('/predicao');
    }
}