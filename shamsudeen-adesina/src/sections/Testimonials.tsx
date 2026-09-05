import { FadeUp } from '../components/FadeUp';
import { testimonials } from '../content';

export function Testimonials() {
  return (
    <section id="testimonials" className="section section--glass">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">Testimonials</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          What clients say.
        </FadeUp>

        <div className="quotes">
          {testimonials.map((t, i) => (
            <FadeUp key={t.author} className="quote" delay={0.08 * i}>
              <p className="quote__text">“{t.quote}”</p>
              <span className="quote__author">— {t.author}</span>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
