const items = [
  'AI Agents',
  'Workflow Automation',
  'LLM Integrations',
  'Data Pipelines',
  'CRM Automation',
  'Voice & Chat Bots',
  'Internal Tools',
  'RAG Systems',
];

export function Marquee() {
  const doubled = [...items, ...items];
  return (
    <div className="marquee" aria-hidden="true">
      <div className="marquee__track">
        {doubled.map((item, i) => (
          <span key={i} className="marquee__item">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
