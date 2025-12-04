// frontend/config.js
window.AppConfig = {
    // API Gateway (Integration Service)
    apiBaseUrl: 'http://127.0.0.1:8000',

    // Log Audit Service (Direct access if needed, or via gateway)
    logApiBaseUrl: 'http://127.0.0.1:8002',

    // Feature Flags
    enableMock: false
};
