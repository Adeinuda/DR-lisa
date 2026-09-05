import { FadeUp } from '../components/FadeUp';

const steps = [
  {
    title: 'Audit',
    body: 'We sit with your team, map every repetitive task and score them by time saved, risk and complexity. You leave with a clear automation roadmap.',
  },
  {
    title: 'Design',
    body: 'Architecture, data flow, model selection and guardrails — documented before a single line is written so there are no surprises.',
  },
  {
    title: 'Build',
    body: 'Rapid iterative builds with weekly demos. Every system ships with logging, error handling and human-in-the-loop checkpoints.',
  },
  {
    title: 'Deploy & Scale',
    body: 'We launch, monitor and optimise. As your business grows, your systems grow with it — we stay on as your automation team.',
  },
];

const stats = [
  { value: '40+', label: 'Systems shipped' },
  { value: '10k+', label: 'Hours automated' },
  { value: '24/7', label: 'Agents running' },
  { value: '1', label: 'Point of contact' },
];

export function Process() {
  return (
    <section id="process" className="section section--glass">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">How we work</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          A simple process. Serious results.
        </FadeUp>

        <div className="steps">
          {steps.map((s, i) => (
            <FadeUp key={s.title} className="step" delay={0.05 * i}>
              <span className="step__num">{String(i + 1).padStart(2, '0')}</span>
              <h3 className="step__title">{s.title}</h3>
              <p className="step__body">{s.body}</p>
            </FadeUp>
          ))}
        </div>

        <div className="stats">
          {stats.map((s, i) => (
            <FadeUp key={s.label} delay={0.08 * i}>
              <div className="stat__value">{s.value}</div>
              <div className="stat__label">{s.label}</div>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
