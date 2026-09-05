import { FadeUp } from '../components/FadeUp';
import { tools } from '../content';

export function Tools() {
  return (
    <section id="stack" className="section section--glass">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">Tech stack</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          Trusted tools & platforms.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.2}>
          Every automation is built using battle-tested, enterprise-grade tools that integrate
          seamlessly into your existing stack.
        </FadeUp>

        <div className="tools">
          {tools.map((t, i) => (
            <FadeUp key={t.name} className="tool" delay={0.04 * i}>
              <span className="tool__name">{t.name}</span>
              <span className="tool__desc">{t.desc}</span>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
