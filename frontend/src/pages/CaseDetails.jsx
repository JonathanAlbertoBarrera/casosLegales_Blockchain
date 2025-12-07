import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  FileText, 
  Users, 
  Calendar, 
  Scale,
  Clock,
  CheckCircle,
  Upload,
  Gavel,
  Plus
} from 'lucide-react';
import { casesAPI } from '../services/api';
import './CaseDetails.css';

const CaseDetails = () => {
  const { caseId } = useParams();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Estados para modales
  const [showDocumentModal, setShowDocumentModal] = useState(false);
  const [showHearingModal, setShowHearingModal] = useState(false);
  const [showJudgmentModal, setShowJudgmentModal] = useState(false);

  useEffect(() => {
    loadCaseDetails();
  }, [caseId]);

  const loadCaseDetails = async () => {
    try {
      const response = await casesAPI.getById(caseId);
      setCaseData(response.data.case);
      setHistory(response.data.history);
    } catch (error) {
      console.error('Error cargando caso:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando detalles del caso...</p>
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="error-container">
        <p>Caso no encontrado</p>
        <button onClick={() => navigate('/dashboard')} className="btn btn-primary">
          Volver al Dashboard
        </button>
      </div>
    );
  }

  const getStatusColor = (status) => {
    const colors = {
      presentado: '#3b82f6',
      en_proceso: '#f59e0b',
      resuelto: '#10b981'
    };
    return colors[status] || '#64748b';
  };

  const getTypeColor = (type) => {
    const colors = {
      civil: '#3b82f6',
      penal: '#ef4444',
      laboral: '#10b981'
    };
    return colors[type] || '#64748b';
  };

  return (
    <div className="case-details-page">
      <div className="case-details-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          <ArrowLeft size={20} />
          Volver
        </button>
        <h1>Detalles del Caso</h1>
        <div className="case-actions">
          {caseData.status !== 'resuelto' && (
            <>
              <button onClick={() => setShowDocumentModal(true)} className="btn btn-outline">
                <Upload size={18} />
                Agregar Documento
              </button>
              <button onClick={() => setShowHearingModal(true)} className="btn btn-outline">
                <Calendar size={18} />
                Programar Audiencia
              </button>
              <button onClick={() => setShowJudgmentModal(true)} className="btn btn-primary">
                <Gavel size={18} />
                Emitir Sentencia
              </button>
            </>
          )}
        </div>
      </div>

      <div className="case-details-content">
        {/* Información principal */}
        <div className="card case-info-card">
          <div className="case-header-info">
            <div>
              <h2>{caseId}</h2>
              <div className="case-badges">
                <span 
                  className="badge"
                  style={{ background: `white`, color: getTypeColor(caseData.type) }}
                >
                  {caseData.type.toUpperCase()}
                </span>
                <span 
                  className="badge"
                  style={{ background: `white`, color: getStatusColor(caseData.status) }}
                >
                  {caseData.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
            </div>
          </div>

          <div className="info-grid">
            <div className="info-item">
              <Users size={20} color="white" />
              <div>
                <p className="info-label">Partes Involucradas</p>
                <p className="info-value">Demandante: {caseData.parties.plaintiff}</p>
                <p className="info-value">Demandado: {caseData.parties.defendant}</p>
              </div>
            </div>

            <div className="info-item">
              <Scale size={20} color="white" />
              <div>
                <p className="info-label">Juez Asignado</p>
                <p className="info-value">{caseData.judge}</p>
              </div>
            </div>

            <div className="info-item">
              <Clock size={20} color="white" />
              <div>
                <p className="info-label">Fecha de Creación</p>
                <p className="info-value">{new Date(caseData.created_at).toLocaleString('es-MX')}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Documentos */}
        {caseData.documents && caseData.documents.length > 0 && (
          <div className="card">
            <h3>
              <FileText size={20} />
              Documentos ({caseData.documents.length})
            </h3>
            <div className="documents-list">
              {caseData.documents.map((doc, index) => (
                <div key={index} className="document-item">
                  <FileText size={18} />
                  <div className="document-info">
                    <p className="document-name">{doc.name}</p>
                    <p className="document-meta">
                      Hash: {doc.hash.substring(0, 16)}...
                      {' | '}
                      Subido por: {doc.uploader}
                      {' | '}
                      {new Date(doc.date).toLocaleDateString('es-MX')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Audiencias */}
        {caseData.hearings && caseData.hearings.length > 0 && (
          <div className="card">
            <h3>
              <Calendar size={20} />
              Audiencias ({caseData.hearings.length})
            </h3>
            <div className="hearings-list">
              {caseData.hearings.map((hearing, index) => (
                <div key={index} className="hearing-item">
                  <Calendar size={18} />
                  <div className="hearing-info">
                    <p className="hearing-type">{hearing.type}</p>
                    <p className="hearing-meta">
                      {hearing.date} - {hearing.location}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Sentencia */}
        {caseData.judgment && (
          <div className="card judgment-card">
            <h3>
              <CheckCircle size={20} />
              Sentencia
            </h3>
            <div className="judgment-info">
              <p><strong>Fallo:</strong> {caseData.judgment.ruling}</p>
              <p><strong>Veredicto:</strong> {caseData.judgment.verdict}</p>
              <p><strong>Detalles:</strong> {caseData.judgment.details}</p>
              <p className="judgment-date">
                Fecha: {new Date(caseData.judgment.date).toLocaleDateString('es-MX')}
              </p>
            </div>
          </div>
        )}

        {/* Historial de Blockchain */}
        <div className="card">
          <h3>Historial en Blockchain</h3>
          <div className="timeline">
            {history.map((entry, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-marker"></div>
                <div className="timeline-content">
                  <p className="timeline-action">{entry.action.replace('_', ' ').toUpperCase()}</p>
                  <p className="timeline-block">Bloque #{entry.block} - {entry.block_hash}</p>
                  <p className="timeline-date">{new Date(entry.timestamp).toLocaleString('es-MX')}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Modal: Agregar Documento */}
      {showDocumentModal && (
        <DocumentModal 
          caseId={caseId}
          onClose={() => setShowDocumentModal(false)}
          onSuccess={() => {
            setShowDocumentModal(false);
            loadCaseDetails();
          }}
        />
      )}

      {/* Modal: Programar Audiencia */}
      {showHearingModal && (
        <HearingModal 
          caseId={caseId}
          onClose={() => setShowHearingModal(false)}
          onSuccess={() => {
            setShowHearingModal(false);
            loadCaseDetails();
          }}
        />
      )}

      {/* Modal: Emitir Sentencia */}
      {showJudgmentModal && (
        <JudgmentModal 
          caseId={caseId}
          onClose={() => setShowJudgmentModal(false)}
          onSuccess={() => {
            setShowJudgmentModal(false);
            loadCaseDetails();
          }}
        />
      )}
    </div>
  );
};

// Modal para agregar documento
const DocumentModal = ({ caseId, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    name: '',
    content: '',
    uploader: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await casesAPI.addDocument(caseId, formData);
      onSuccess();
    } catch (error) {
      console.error('Error agregando documento:', error);
      alert('Error al agregar documento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2><FileText size={24} /> Agregar Documento</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nombre del Documento</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Ej: Demanda inicial"
              required
            />
          </div>
          <div className="form-group">
            <label>Contenido/Descripción</label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({...formData, content: e.target.value})}
              placeholder="Descripción o contenido del documento..."
              rows={4}
              required
            />
          </div>
          <div className="form-group">
            <label>Subido por</label>
            <input
              type="text"
              value={formData.uploader}
              onChange={(e) => setFormData({...formData, uploader: e.target.value})}
              placeholder="Nombre de quien sube el documento"
              required
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Agregando...' : 'Agregar Documento'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Modal para programar audiencia
const HearingModal = ({ caseId, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    type: '',
    date: '',
    location: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await casesAPI.scheduleHearing(caseId, formData);
      onSuccess();
    } catch (error) {
      console.error('Error programando audiencia:', error);
      alert('Error al programar audiencia');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2><Calendar size={24} /> Programar Audiencia</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Tipo de Audiencia</label>
            <input
              type="text"
              value={formData.type}
              onChange={(e) => setFormData({...formData, type: e.target.value})}
              placeholder="Ej: Audiencia preliminar, Juicio oral, etc."
              required
            />
          </div>
          <div className="form-group">
            <label>Fecha y Hora</label>
            <input
              type="datetime-local"
              value={formData.date}
              onChange={(e) => setFormData({...formData, date: e.target.value})}
              required
            />
          </div>
          <div className="form-group">
            <label>Ubicación</label>
            <input
              type="text"
              value={formData.location}
              onChange={(e) => setFormData({...formData, location: e.target.value})}
              placeholder="Ej: Sala 3, Tribunal de Justicia"
              required
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Programando...' : 'Programar Audiencia'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Modal para emitir sentencia
const JudgmentModal = ({ caseId, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    ruling: '',
    verdict: '',
    details: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await casesAPI.issueJudgment(caseId, formData);
      onSuccess();
    } catch (error) {
      console.error('Error emitiendo sentencia:', error);
      alert('Error al emitir sentencia');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2><Gavel size={24} /> Emitir Sentencia</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Fallo</label>
            <input
              type="text"
              value={formData.ruling}
              onChange={(e) => setFormData({...formData, ruling: e.target.value})}
              placeholder="Ej: A favor del demandante"
              required
            />
          </div>
          <div className="form-group">
            <label>Veredicto</label>
            <select
              value={formData.verdict}
              onChange={(e) => setFormData({...formData, verdict: e.target.value})}
              required
            >
              <option value="">Seleccionar...</option>
              <option value="Culpable">Culpable</option>
              <option value="Inocente">Inocente</option>
              <option value="A favor del demandante">A favor del demandante</option>
              <option value="A favor del demandado">A favor del demandado</option>
            </select>
          </div>
          <div className="form-group">
            <label>Detalles de la Sentencia</label>
            <textarea
              value={formData.details}
              onChange={(e) => setFormData({...formData, details: e.target.value})}
              placeholder="Fundamentos legales, argumentos y detalles..."
              rows={6}
              required
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn btn-outline">
              Cancelar
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Emitiendo...' : 'Emitir Sentencia'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CaseDetails;
