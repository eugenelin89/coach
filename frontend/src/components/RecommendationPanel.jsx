import React from 'react';
import '../styles/RecommendationPanel.css';

const Placeholder = () => (
  <div className="placeholder">
    <h2>Your insight hub</h2>
    <p>
      Submit the current play details to reveal a tailored recommendation including pitch selection,
      alignment adjustments, and the signals to relay.
    </p>
    <ul>
      <li>Strategic pitch call with supporting rationale.</li>
      <li>Defensive positioning cues for every infielder.</li>
      <li>Signals for both the hitter and on-base runners.</li>
    </ul>
  </div>
);

const RecommendationPanel = ({ recommendation, isSubmitting }) => {
  if (isSubmitting) {
    return (
      <section className="recommendation">
        <div className="loading">
          <span className="spinner" aria-hidden="true" />
          <p>Crunching spray charts and matchup data...</p>
        </div>
      </section>
    );
  }

  if (!recommendation) {
    return (
      <section className="recommendation">
        <Placeholder />
      </section>
    );
  }

  const { pitch_call, catcher_plan, defensive_alignment, offensive_signs, key_points } = recommendation;

  return (
    <section className="recommendation">
      <header>
        <p className="eyebrow">Recommended play</p>
        <h2>{pitch_call}</h2>
        <p className="catcher-plan">{catcher_plan}</p>
      </header>

      <div className="alignment">
        <h3>Defensive alignment</h3>
        <dl>
          {Object.entries(defensive_alignment).map(([position, detail]) => (
            <div className="alignment-row" key={position}>
              <dt>{position}</dt>
              <dd>{detail}</dd>
            </div>
          ))}
        </dl>
      </div>

      <div className="signals">
        <h3>Signals to relay</h3>
        <div className="signal-grid">
          <div className="signal-card">
            <h4>Hitter</h4>
            <p>{offensive_signs.hitter || 'No special sign required.'}</p>
          </div>
          <div className="signal-card">
            <h4>Runners</h4>
            <p>{offensive_signs.runner || 'Hold position and read the ball.'}</p>
          </div>
        </div>
      </div>

      {key_points?.length ? (
        <div className="key-points">
          <h3>Key points</h3>
          <ul>
            {key_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
};

export default RecommendationPanel;
