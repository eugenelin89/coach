import React from 'react';
import '../styles/StatusBanner.css';

const StatusBanner = ({ isSubmitting, error }) => {
  if (error) {
    return (
      <div className="status-banner error" role="alert">
        <span aria-hidden="true">⚠️</span>
        <p>{error}</p>
      </div>
    );
  }

  if (isSubmitting) {
    return (
      <div className="status-banner info" role="status">
        <span className="spinner" aria-hidden="true" />
        <p>Generating recommendation...</p>
      </div>
    );
  }

  return (
    <div className="status-banner success">
      <span aria-hidden="true">✨</span>
      <p>Ready when you are—complete the form to get started.</p>
    </div>
  );
};

export default StatusBanner;
