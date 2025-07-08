import React from 'react';
import Agent0Diagnostic from '../components/agentes/Agent0Diagnostic';
import Agent1Keywords from '../components/agentes/Agent1Keywords';
import Agent2Resume from '../components/agentes/Agent2Resume';
import Agent3Linkedin from '../components/agentes/Agent3Linkedin';
import Agent4Content from '../components/agentes/Agent4Content';

const AgentesPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Agentes</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Agent0Diagnostic />
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Agent1Keywords />
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Agent2Resume />
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Agent3Linkedin />
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Agent4Content />
        </div>
      </div>
    </div>
  );
};

export default AgentesPage;