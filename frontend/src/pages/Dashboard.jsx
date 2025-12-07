import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Scale, 
  Briefcase, 
  FileText, 
  TrendingUp, 
  Shield,
  Users,
  Clock,
  CheckCircle,
  AlertCircle,
  Plus,
  Eye,
  Search
} from 'lucide-react';
import { casesAPI, blockchainAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import CreateCaseModal from '../components/CreateCaseModal';
import './Dashboard.css';

const Dashboard = () => {
  const [cases, setCases] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [casesRes, statsRes] = await Promise.all([
        casesAPI.getAll(),
        blockchainAPI.getStatistics()
      ]);
      
      setCases(Object.entries(casesRes.data.cases).map(([id, data]) => ({
        id,
        ...data
      })));
      setStatistics(statsRes.data.statistics);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      presentado: { class: 'badge-info', text: 'Presentado' },
      en_proceso: { class: 'badge-warning', text: 'En Proceso' },
      resuelto: { class: 'badge-success', text: 'Resuelto' }
    };
    
    const config = statusConfig[status] || statusConfig.presentado;
    return <span className={`badge ${config.class}`}>{config.text}</span>;
  };

  const getTypeBadge = (type) => {
    const typeColors = {
      civil: '#3b82f6',
      penal: '#ef4444',
      laboral: '#10b981'
    };
    
    return (
      <span 
        className="type-badge" 
        style={{ background: `${typeColors[type]}20`, color: typeColors[type] }}
      >
        {type.toUpperCase()}
      </span>
    );
  };

  const filteredCases = cases.filter(c => 
    c.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando sistema judicial...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <Scale size={32} color="#1e3a8a" />
            <div>
              <h1>Sistema Judicial Blockchain</h1>
              <p>Gestión Transparente de Casos</p>
            </div>
          </div>
          <div className="header-right">
            <div className="user-info">
              <Users size={20} />
              <div>
                <p className="user-name">{user?.full_name}</p>
                <p className="user-role">{user?.role}</p>
              </div>
            </div>
            <button onClick={handleLogout} className="btn btn-outline">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        {/* Statistics Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#dbeafe' }}>
              <Briefcase size={24} color="#1e40af" />
            </div>
            <div className="stat-info">
              <h3>{statistics?.total_cases || 0}</h3>
              <p>Casos Totales</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#fef3c7' }}>
              <Clock size={24} color="#92400e" />
            </div>
            <div className="stat-info">
              <h3>{statistics?.cases_by_status?.en_proceso || 0}</h3>
              <p>En Proceso</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#d1fae5' }}>
              <CheckCircle size={24} color="#065f46" />
            </div>
            <div className="stat-info">
              <h3>{statistics?.cases_by_status?.resuelto || 0}</h3>
              <p>Resueltos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#e0e7ff' }}>
              <Shield size={24} color="#4338ca" />
            </div>
            <div className="stat-info">
              <h3>{statistics?.total_blocks || 0}</h3>
              <p>Bloques en Cadena</p>
            </div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="action-bar">
          <div className="search-box">
            <Search size={20} />
            <input
              type="text"
              placeholder="Buscar casos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input"
            />
          </div>
          <div className="action-buttons">
            <button 
              onClick={() => setShowCreateModal(true)} 
              className="btn btn-primary"
            >
              <Plus size={20} />
              Nuevo Caso
            </button>
            <button 
              onClick={() => navigate('/blockchain')} 
              className="btn btn-outline"
            >
              <Shield size={20} />
              Ver Blockchain
            </button>
          </div>
        </div>

        {/* Cases Table */}
        <div className="card">
          <div className="card-header">
            <h2>
              <FileText size={24} />
              Casos Judiciales
            </h2>
          </div>

          {filteredCases.length === 0 ? (
            <div className="empty-state">
              <AlertCircle size={48} color="#94a3b8" />
              <p>No se encontraron casos</p>
              <button 
                onClick={() => setShowCreateModal(true)} 
                className="btn btn-primary"
              >
                Crear Primer Caso
              </button>
            </div>
          ) : (
            <div className="cases-table">
              <table>
                <thead>
                  <tr>
                    <th>ID de Caso</th>
                    <th>Tipo</th>
                    <th>Estado</th>
                    <th>Juez</th>
                    <th>Documentos</th>
                    <th>Audiencias</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCases.map((case_) => (
                    <tr key={case_.id} className="slide-in">
                      <td>
                        <strong>{case_.id}</strong>
                      </td>
                      <td>{getTypeBadge(case_.type)}</td>
                      <td>{getStatusBadge(case_.status)}</td>
                      <td className="judge-cell">
                        {case_.judge.substring(0, 30)}...
                      </td>
                      <td>
                        <span className="count-badge">
                          {case_.documents.length}
                        </span>
                      </td>
                      <td>
                        <span className="count-badge">
                          {case_.hearings.length}
                        </span>
                      </td>
                      <td>
                        <button
                          onClick={() => navigate(`/cases/${case_.id}`)}
                          className="btn-icon"
                          title="Ver detalles"
                        >
                          <Eye size={18} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Blockchain Status */}
        <div className="blockchain-status card">
          <div className="status-header">
            <Shield size={24} color="white" />
            <h3>Estado de la Blockchain</h3>
          </div>
          <div className="status-grid">
            <div className="status-item">
              <p className="status-label">Total Bloques</p>
              <p className="status-value">{statistics?.total_blocks || 0}</p>
            </div>
            <div className="status-item">
              <p className="status-label">Transacciones</p>
              <p className="status-value">{statistics?.total_transactions || 0}</p>
            </div>
            <div className="status-item">
              <p className="status-label">Dificultad</p>
              <p className="status-value">{statistics?.difficulty || 3}</p>
            </div>
            <div className="status-item">
              <p className="status-label">Integridad</p>
              <p className="status-value">✓ Verificada</p>
            </div>
          </div>
        </div>
      </div>

      {/* Modal para crear caso */}
      <CreateCaseModal 
        isOpen={showCreateModal} 
        onClose={() => setShowCreateModal(false)}
        onCaseCreated={loadData}
      />
    </div>
  );
};

export default Dashboard;
