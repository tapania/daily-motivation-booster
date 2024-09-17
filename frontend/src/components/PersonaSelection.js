// src/components/PersonaSelection.js
import React from 'react';
import { personas } from '../personas';

function PersonaSelection({ selectedPersona, setSelectedPersona }) {
  return (
    <select
      className="select select-bordered w-full"
      value={selectedPersona}
      onChange={e => setSelectedPersona(e.target.value)}
    >
      <option value="">Select a Persona</option>
      {personas.map(persona => (
        <option key={persona.name} value={persona.name}>
          {persona.name} - {persona.tone}
        </option>
      ))}
    </select>
  );
}

export default PersonaSelection;
