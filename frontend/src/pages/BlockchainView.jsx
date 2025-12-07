import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Box, Link as LinkIcon, CheckCircle, XCircle } from 'lucide-react';
import { blockchainAPI } from '../services/api';
import './BlockchainView.css';

const BlockchainView = () => {
  const navigate = useNavigate();
  const [blocks, setBlocks] = useState([]);
  const [isValid, setIsValid] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBlockchain();
    verifyBlockchain();
  }, []);

  const loadBlockchain = async () => {
    try {
      const response = await blockchainAPI.getChain();
      setBlocks(response.data.chain);
    } catch (error) {
      console.error('Error cargando blockchain:', error);
    } finally {
      setLoading(false);
    }
  };

  const verifyBlockchain = async () => {
    try {
      const response = await blockchainAPI.verify();
      setIsValid(response.data.valid);
    } catch (error) {
      console.error('Error verificando blockchain:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando blockchain...</p>
      </div>
    );
  }

  return (
    <div className="blockchain-view-page">
      <div className="blockchain-header">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          <ArrowLeft size={20} />
          Volver
        </button>
        <h1>Explorador de Blockchain</h1>
      </div>

      <div className="blockchain-content">
        {/* Estado de validación */}
        <div className={`validation-card ${isValid ? 'valid' : 'invalid'}`}>
          {isValid ? (
            <>
              <CheckCircle size={48} />
              <div>
                <h3>Blockchain Válida</h3>
                <p>Todos los bloques están correctamente encadenados</p>
              </div>
            </>
          ) : (
            <>
              <XCircle size={48} />
              <div>
                <h3>Blockchain Inválida</h3>
                <p>Se detectaron inconsistencias en la cadena</p>
              </div>
            </>
          )}
        </div>

        {/* Lista de bloques */}
        <div className="blocks-container">
          {blocks.map((block, index) => (
            <div key={block.index} className="block-card">
              <div className="block-header">
                <div className="block-title">
                  <Box size={24} />
                  <h3>Bloque #{block.index}</h3>
                </div>
                {block.index === 0 && (
                  <span className="genesis-badge">GÉNESIS</span>
                )}
              </div>

              <div className="block-info">
                <div className="info-row">
                  <span className="label">Hash:</span>
                  <code className="hash">{block.hash}</code>
                </div>
                <div className="info-row">
                  <span className="label">Hash Anterior:</span>
                  <code className="hash">{block.previous_hash || 'N/A'}</code>
                </div>
                <div className="info-row">
                  <span className="label">Timestamp:</span>
                  <span>{new Date(block.timestamp).toLocaleString('es-MX')}</span>
                </div>
                <div className="info-row">
                  <span className="label">Nonce:</span>
                  <span>{block.nonce}</span>
                </div>
                <div className="info-row">
                  <span className="label">Transacciones:</span>
                  <span>{block.transactions.length}</span>
                </div>
              </div>

              {/* Transacciones */}
              {block.transactions.length > 0 && (
                <div className="transactions-section">
                  <h4>Transacciones</h4>
                  {block.transactions.map((tx, txIndex) => (
                    <div key={txIndex} className="transaction-item">
                      <div className="tx-header">
                        <span className="tx-action">{tx.action.replace('_', ' ').toUpperCase()}</span>
                        <span className="tx-case">{tx.case_id}</span>
                      </div>
                      <div className="tx-details">
                        <p><strong>Partes:</strong> {tx.parties.plaintiff} vs {tx.parties.defendant}</p>
                        <p><strong>Juez:</strong> {tx.judge}</p>
                        <p className="tx-time">{new Date(tx.timestamp).toLocaleString('es-MX')}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Conexión al siguiente bloque */}
              {index < blocks.length - 1 && (
                <div className="block-connection">
                  <LinkIcon size={20} />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Resumen */}
        <div className="blockchain-summary">
          <div className="summary-card">
            <h4>Total de Bloques</h4>
            <p className="summary-value">{blocks.length}</p>
          </div>
          <div className="summary-card">
            <h4>Total de Transacciones</h4>
            <p className="summary-value">
              {blocks.reduce((sum, block) => sum + block.transactions.length, 0)}
            </p>
          </div>
          <div className="summary-card">
            <h4>Estado</h4>
            <p className="summary-value" style={{ color: isValid ? '#10b981' : '#ef4444' }}>
              {isValid ? 'Válida ✓' : 'Inválida ✗'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockchainView;
