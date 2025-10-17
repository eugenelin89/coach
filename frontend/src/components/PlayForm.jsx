import React, { useMemo, useState } from 'react';
import '../styles/PlayForm.css';

const DEFAULT_STATE = {
  offense_team: '',
  defense_team: '',
  inning: 1,
  half_inning: 'top',
  outs: 0,
  balls: 0,
  strikes: 0,
  runners_on_first: false,
  runners_on_second: false,
  runners_on_third: false,
  score_difference: 0,
  context_notes: '',
  save_to_history: true,
};

const numericFields = ['inning', 'outs', 'balls', 'strikes', 'score_difference'];

const PlayForm = ({ onSubmit, isSubmitting }) => {
  const [formState, setFormState] = useState(DEFAULT_STATE);

  const handleChange = (event) => {
    const { name, type, value, checked } = event.target;
    let nextValue = type === 'checkbox' ? checked : value;
    if (numericFields.includes(name)) {
      nextValue = Number(nextValue);
    }
    setFormState((prev) => ({ ...prev, [name]: nextValue }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formState);
  };

  const canSubmit = useMemo(() => {
    return (
      formState.offense_team.trim().length > 0 &&
      formState.defense_team.trim().length > 0 &&
      Number.isFinite(formState.inning) &&
      formState.inning > 0 &&
      Number.isFinite(formState.outs) &&
      Number.isFinite(formState.balls) &&
      Number.isFinite(formState.strikes)
    );
  }, [formState]);

  const handleReset = () => setFormState(DEFAULT_STATE);

  return (
    <form className="play-form" onSubmit={handleSubmit}>
      <div className="form-header">
        <h2>Game situation</h2>
        <p>Fill in the current game state to generate a contextual recommendation.</p>
      </div>

      <div className="grid">
        <label className="field">
          <span>Offense team</span>
          <input
            name="offense_team"
            type="text"
            placeholder="E.g. Wildcats"
            value={formState.offense_team}
            onChange={handleChange}
            required
          />
        </label>

        <label className="field">
          <span>Defense team</span>
          <input
            name="defense_team"
            type="text"
            placeholder="E.g. Falcons"
            value={formState.defense_team}
            onChange={handleChange}
            required
          />
        </label>

        <label className="field">
          <span>Inning</span>
          <input
            name="inning"
            type="number"
            min="1"
            value={formState.inning}
            onChange={handleChange}
          />
        </label>

        <label className="field">
          <span>Half inning</span>
          <select name="half_inning" value={formState.half_inning} onChange={handleChange}>
            <option value="top">Top</option>
            <option value="bottom">Bottom</option>
          </select>
        </label>

        <label className="field">
          <span>Outs</span>
          <input name="outs" type="number" min="0" max="2" value={formState.outs} onChange={handleChange} />
        </label>

        <label className="field">
          <span>Balls</span>
          <input name="balls" type="number" min="0" max="3" value={formState.balls} onChange={handleChange} />
        </label>

        <label className="field">
          <span>Strikes</span>
          <input name="strikes" type="number" min="0" max="2" value={formState.strikes} onChange={handleChange} />
        </label>

        <label className="field">
          <span>Score difference</span>
          <input
            name="score_difference"
            type="number"
            value={formState.score_difference}
            onChange={handleChange}
          />
        </label>
      </div>

      <div className="runner-grid">
        <p className="section-title">Runners on base</p>
        <label className="checkbox">
          <input name="runners_on_first" type="checkbox" checked={formState.runners_on_first} onChange={handleChange} />
          <span>First base</span>
        </label>
        <label className="checkbox">
          <input name="runners_on_second" type="checkbox" checked={formState.runners_on_second} onChange={handleChange} />
          <span>Second base</span>
        </label>
        <label className="checkbox">
          <input name="runners_on_third" type="checkbox" checked={formState.runners_on_third} onChange={handleChange} />
          <span>Third base</span>
        </label>
      </div>

      <label className="field">
        <span>Context notes</span>
        <textarea
          name="context_notes"
          placeholder="Pitcher tendencies, weather factors, hitter scouting notes..."
          value={formState.context_notes}
          onChange={handleChange}
          rows="4"
        />
      </label>

      <label className="checkbox save-checkbox">
        <input name="save_to_history" type="checkbox" checked={formState.save_to_history} onChange={handleChange} />
        <span>Save this play to the game history once submitted</span>
      </label>

      <div className="form-actions">
        <button type="submit" className="primary" disabled={!canSubmit || isSubmitting}>
          {isSubmitting ? 'Generating...' : 'Generate recommendation'}
        </button>
        <button type="button" className="ghost" onClick={handleReset} disabled={isSubmitting}>
          Reset form
        </button>
      </div>
    </form>
  );
};

export default PlayForm;
