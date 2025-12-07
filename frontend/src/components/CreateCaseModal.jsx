import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { casesAPI, judgesAPI } from '../services/api';
import './CreateCaseModal.css';

const CreateCaseModal = ({ isOpen, onClose, onCaseCreated }) => {
  const [formData, setFormData] = useState({
    case_id: '',
    case_type: 'civil',
    plaintiff_name: '',
    defendant_name: '',
    judge_id: '',
    description: ''
  });
  const [judges, setJudges] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      loadJudges();
    }
  }, [isOpen]);

  const loadJudges = async () => {
    try {
      const response = await judgesAPI.getAll();
      setJudges(response.data.judges);
      // Seleccionar el primer juez por defecto
      if (Object.keys(response.data.judges).length > 0) {
        setFormData(prev => ({
          ...prev,
          judge_id: Object.keys(response.data.judges)[0]
        }));
      }
    } catch (err) {
      console.error('Error cargando jueces:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await casesAPI.create(formData);
      onCaseCreated();
      onClose();
      // Reset form
      setFormData({
        case_id: '',
        case_type: 'civil',
        plaintiff_name: '',
        defendant_name: '',
        judge_id: Object.keys(judges)[0] || '',
        description: ''
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Error al crear caso');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Crear Nuevo Caso Judicial</h2>
          <button onClick={onClose} className="modal-close">
            <X size={24} />
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="case_id">ID del Caso *</label>
            <input
              id="case_id"
              name="case_id"
              type="text"
              className="input"
              placeholder="EXP-2024-001"
              value={formData.case_id}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="case_type">Tipo de Caso *</label>
            <select
              id="case_type"
              name="case_type"
              className="input"
              value={formData.case_type}
              onChange={handleChange}
              required
            >
              <option value="civil">Civil</option>
              <option value="penal">Penal</option>
              <option value="laboral">Laboral</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="plaintiff_name">Demandante *</label>
            <input
              id="plaintiff_name"
              name="plaintiff_name"
              type="text"
              className="input"
              placeholder="Nombre del demandante"
              value={formData.plaintiff_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="defendant_name">Demandado *</label>
            <input
              id="defendant_name"
              name="defendant_name"
              type="text"
              className="input"
              placeholder="Nombre del demandado"
              value={formData.defendant_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="judge_id">Juez Asignado *</label>
            <select
              id="judge_id"
              name="judge_id"
              className="input"
              value={formData.judge_id}
              onChange={handleChange}
              required
            >
              {Object.entries(judges).map(([id, specialty]) => (
                <option key={id} value={id}>
                  {id} - {specialty}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="description">Descripción *</label>
            <textarea
              id="description"
              name="description"
              className="input"
              placeholder="Descripción detallada del caso"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              required
            />
          </div>

          <div className="modal-actions">
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Creando...' : 'Crear Caso'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateCaseModal;
