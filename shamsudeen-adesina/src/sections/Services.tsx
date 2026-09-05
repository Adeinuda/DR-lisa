import { FadeUp } from '../components/FadeUp';

const services = [
  {
    title: 'AI Agents & Assistants',
    body: 'Autonomous agents that read your inbox, qualify leads, answer customers and take action across your tools — 24 hours a day.',
  },
  {
    title: 'Workflow Automation',
    body: 'We map the repetitive work in your business and replace it with reliable pipelines built on n8n, Make, Zapier or custom code.',
  },
  {
    title: 'LLM Integrations',
    body: 'OpenAI, Anthropic, Gemini and open-source models wired directly into your product, CRM and internal systems.',
  },
  {
    title: 'Knowledge & RAG Systems',
    body: 'Chat with your documents, SOPs and databases. Private retrieval systems that give accurate, sourced answers.',
  },
  {
    title: 'Data Pipelines',
    body: 'Scraping, enrichment, cleaning and syncing. Data that flows automatically from where it lives to where it is needed.',
  },
  {
    title: 'Custom Internal Tools',
    body: 'Dashboards, approval flows and back-office apps built around your team — not the other way around.',
  },
];

export function Services() {
  return (
    <section id="services" className="section">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">What we do</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          One partner for every layer of your automation stack.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.2}>
          From the first process audit to the last deployed agent, we design, build and maintain
          systems that remove manual work and compound over time.
        </FadeUp>

        <div className="grid">
          {services.map((s, i) => (
            <FadeUp key={s.title} className="card" delay={0.05 * i}>
              <span className="card__index">{String(i + 1).padStart(2, '0')}</span>
              <div>
                <h3 className="card__title">{s.title}</h3>
                <p className="card__body">{s.body}</p>
              </div>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
