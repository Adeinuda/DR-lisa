import { FadeUp } from '../components/FadeUp';
import { steps, stats } from '../content';

export function Process() {
  return (
    <section id="process" className="section section--glass">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">How it works</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          From discovery to deployment.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.2}>
          A structured, transparent process ensures every automation is built right the first time
          — on time, on spec, and built to scale. Most projects go live in 2–4 weeks.
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
              <div className="stat__note">{s.note}</div>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
