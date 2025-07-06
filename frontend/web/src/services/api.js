const getApiBaseUrl = () => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:8000';
    }
    else {
        return 'https://api.leaseboost.fr';
    }
}
const API_BASE_URL = getApiBaseUrl();

class ApiService{
    async analyzeLease(file) {
        const formData = new FormData();
        formData.append('file', file);

        // adding timeout for analysis
        const controller = new AbortController();
        const timeoutId = setTimeout( () => controller.abort(), 180000); // 3 minutes

        try {
            const response = await fetch(`${API_BASE_URL}/api/analyze-lease/`, {
                method: 'POST',
                body: formData,
                signal: controller.signal,
            });

            clearTimeout(timeoutId);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erreur lors de l\'analyse du bail');
            }

            return response.json();
        } catch (error) {
            clearTimeout(timeoutId);

            if(error.name === 'AbortError'){
                throw new Error('Analyse trop longue - Veuillez réessayer avec un document plus petit');
            }

            throw error;
        }
    }

    async healthCheck() {
        const response = await fetch(`${API_BASE_URL}/api/health-check/`);
        return response.json();
    }
}

export default new ApiService();