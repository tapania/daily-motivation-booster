// frontend/src/components/PersonaSelection.js
import React from 'react';
import { personas } from '../personas';

function PersonaSelection({ selectedPersona, onSelectPersona }) {
  return (
    <select
      className="select select-bordered w-full"
      value={selectedPersona}
      onChange={e => onSelectPersona(e.target.value)}
    >
      <option value="">Select a Persona</option>
      {personas.map(persona => (
        <option key={persona.name} value={persona.name}>
          {persona.name} - {persona.tone.length > 50 ? persona.tone.substring(0, 50) + '...' : persona.tone}
        </option>
      ))}
    </select>
  );
}

export default PersonaSelection;
