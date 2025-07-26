import React, { useState, useEffect, useCallback } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import auditService from '../../services/auditService';
import './AuditDashboard.css';

const AuditDashboard = () => {
  const [auditStats, setAuditStats] = useState({});
  const [recentLogs, setRecentLogs] = useState([]);
  const [performanceMetrics, setPerformanceMetrics] = useState([]);
  const [errorLogs, setErrorLogs] = useState([]);
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedLogLevel, setSelectedLogLevel] = useState('all');
  const [autoRefresh, setAutoRefresh] = useState(true);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const refreshData = useCallback(() => {
    const stats = auditService.getAuditStats();
    setAuditStats(stats);

    const recent = auditService.getRecentLogs(100);
    setRecentLogs(recent);

    const errors = auditService.getLogsByLevel('error');
    setErrorLogs(errors.slice(-20));

    // Generar métricas de performance para gráfico
    const perfData = recent
      .filter(log => log.action === 'api_response' && log.details.duration)
      .slice(-20)
      .map((log, index) => ({
        request: index + 1,
        duration: log.details.duration,
        endpoint: log.details.url
      }));
    setPerformanceMetrics(perfData);
  }, []);

  useEffect(() => {
    refreshData();
    
    if (autoRefresh) {
      const interval = setInterval(refreshData, 5000); // Actualizar cada 5 segundos
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshData]);

  const exportLogs = (format) => {
    auditService.exportLogs(format);
    auditService.logAction('AUDIT_LOGS_EXPORTED', { format });
  };

  const clearLogs = () => {
    if (window.confirm('¿Estás seguro de que quieres limpiar los logs de auditoría?')) {
      auditService.logs = [];
      auditService.logAction('AUDIT_LOGS_CLEARED', {});
      refreshData();
    }
  };

  const getFilteredLogs = () => {
    if (selectedLogLevel === 'all') return recentLogs;
    return recentLogs.filter(log => log.level === selectedLogLevel);
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getLogLevelColor = (level) => {
    switch (level) {
      case 'error': return '#ef4444';
      case 'warn': return '#f59e0b';
      case 'info': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  const renderPieData = () => {
    return Object.entries(auditStats.byLevel || {}).map(([level, count]) => ({
      name: level,
      value: count,
      color: getLogLevelColor(level)
    }));
  };

  if (!isExpanded) {
    return (
      <div className="audit-dashboard-collapsed">
        <button 
          onClick={() => setIsExpanded(true)}
          className="audit-toggle-btn"
          title="Abrir Dashboard de Auditoría"
        >
          📊 Auditoría ({auditStats.totalLogs || 0})
        </button>
        {errorLogs.length > 0 && (
          <div className="audit-error-indicator">
            ⚠️ {errorLogs.length} errores
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="audit-dashboard">
      <div className="audit-header">
        <h2>Dashboard de Auditoría en Tiempo Real</h2>
        <div className="audit-controls">
          <label>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-actualizar
          </label>
          <button onClick={refreshData} className="refresh-btn">
            🔄 Actualizar
          </button>
          <button onClick={() => exportLogs('json')} className="export-btn">
            📥 Exportar JSON
          </button>
          <button onClick={() => exportLogs('csv')} className="export-btn">
            📥 Exportar CSV
          </button>
          <button onClick={clearLogs} className="clear-btn">
            🗑️ Limpiar
          </button>
          <button 
            onClick={() => setIsExpanded(false)}
            className="collapse-btn"
            title="Minimizar Dashboard"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="audit-stats">
        <div className="stat-card">
          <h3>Total de Logs</h3>
          <div className="stat-value">{auditStats.totalLogs || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Errores</h3>
          <div className="stat-value error">{auditStats.byLevel?.error || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Advertencias</h3>
          <div className="stat-value warning">{auditStats.byLevel?.warn || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Información</h3>
          <div className="stat-value info">{auditStats.byLevel?.info || 0}</div>
        </div>
      </div>

      <div className="audit-charts">
        <div className="chart-container">
          <h3>Distribución de Logs por Nivel</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={renderPieData()}
                cx="50%"
                cy="50%"
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {renderPieData().map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h3>Performance de API (últimos 20 requests)</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={performanceMetrics}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="request" />
              <YAxis />
              <Tooltip 
                formatter={(value, name, props) => [
                  `${value.toFixed(2)}ms`, 
                  props.payload.endpoint
                ]}
              />
              <Line 
                type="monotone" 
                dataKey="duration" 
                stroke="#8884d8" 
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="audit-logs-section">
        <div className="logs-header">
          <h3>Logs Recientes</h3>
          <select 
            value={selectedLogLevel}
            onChange={(e) => setSelectedLogLevel(e.target.value)}
            className="level-filter"
          >
            <option value="all">Todos los niveles</option>
            <option value="error">Solo errores</option>
            <option value="warn">Solo advertencias</option>
            <option value="info">Solo información</option>
          </select>
        </div>

        <div className="logs-container">
          {getFilteredLogs().slice(-50).reverse().map((log) => (
            <div 
              key={log.id} 
              className={`log-entry ${log.level}`}
              style={{ borderLeftColor: getLogLevelColor(log.level) }}
            >
              <div className="log-timestamp">
                {formatTimestamp(log.timestamp)}
              </div>
              <div className="log-level">
                {log.level.toUpperCase()}
              </div>
              <div className="log-action">
                {log.action}
              </div>
              <div className="log-details">
                {JSON.stringify(log.details || log.error, null, 2)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {errorLogs.length > 0 && (
        <div className="error-summary">
          <h3>Resumen de Errores Recientes</h3>
          <div className="error-list">
            {errorLogs.slice(-10).map((error) => (
              <div key={error.id} className="error-item">
                <span className="error-time">
                  {formatTimestamp(error.timestamp)}
                </span>
                <span className="error-message">
                  {error.error?.message || error.action}
                </span>
                <span className="error-component">
                  {error.component}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AuditDashboard;
