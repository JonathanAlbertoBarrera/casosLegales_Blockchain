import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redireccionar al login si no está autenticado
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Autenticación
export const authAPI = {
  login: (username, password) => 
    api.post('/auth/login', { username, password }),
  
  register: (userData) => 
    api.post('/auth/register', userData),
  
  logout: () => 
    api.post('/auth/logout'),
  
  getCurrentUser: () => 
    api.get('/auth/me'),
};

// Casos judiciales
export const casesAPI = {
  getAll: () => 
    api.get('/cases'),
  
  getById: (caseId) => 
    api.get(`/cases/${caseId}`),
  
  create: (caseData) => 
    api.post('/cases', caseData),
  
  addDocument: (caseId, documentData) => 
    api.post(`/cases/${caseId}/documents`, documentData),
  
  scheduleHearing: (caseId, hearingData) => 
    api.post(`/cases/${caseId}/hearings`, hearingData),
  
  issueJudgment: (caseId, judgmentData) => 
    api.post(`/cases/${caseId}/judgment`, judgmentData),
};

// Jueces
export const judgesAPI = {
  getAll: () => 
    api.get('/judges'),
  
  register: (judgeData) => 
    api.post('/judges', judgeData),
};

// Blockchain
export const blockchainAPI = {
  verify: () => 
    api.get('/blockchain/verify'),
  
  getStatistics: () => 
    api.get('/blockchain/statistics'),
  
  export: () => 
    api.get('/blockchain/export'),
  
  verifyDocument: (caseId, documentContent) => 
    api.post('/documents/verify', { case_id: caseId, document_content: documentContent }),
};

export default api;
