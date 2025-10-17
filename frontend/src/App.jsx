import React, { useState } from 'react';
import PlayForm from './components/PlayForm.jsx';
import RecommendationPanel from './components/RecommendationPanel.jsx';
import StatusBanner from './components/StatusBanner.jsx';
import './styles/App.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
const API_ENDPOINT = `${API_BASE_URL}/api/recommendations/`.replace('//api', '/api');

const App = () => {
  const [recommendation, setRecommendation] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (payload) => {
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.detail || 'Unable to generate recommendation.');
      }

      const data = await response.json();
      setRecommendation(data);
    } catch (err) {
      setRecommendation(null);
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="app-root">
      <div className="app-background" />
      <main className="app-container">
        <header className="app-header">
          <StatusBanner isSubmitting={isSubmitting} error={error} />
          <div className="headline-group">
            <p className="eyebrow">Game Play Coach</p>
            <h1>Craft the next winning call</h1>
            <p className="lede">
              Capture the current game situation, then let the engine surface a data-backed recommendation
              for your next pitch, defensive alignment, and offensive signs.
            </p>
          </div>
        </header>

        <section className="app-grid">
          <article className="panel form-panel">
            <PlayForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
          </article>
          <aside className="panel recommendation-panel">
            <RecommendationPanel recommendation={recommendation} isSubmitting={isSubmitting} />
          </aside>
        </section>
      </main>
    </div>
  );
};

export default App;
