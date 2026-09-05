import { FadeUp } from '../components/FadeUp';
import { services } from '../content';

export function Services() {
  return (
    <section id="services" className="section">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">What I build</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          Services designed to eliminate bottlenecks.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.2}>
          From intelligent chatbots to fully automated CRM pipelines — every service is engineered
          to reduce manual overhead and scale your operations without hiring more staff.
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
