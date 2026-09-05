import { FadeUp } from '../components/FadeUp';

const HEADLINE = 'WE BUILD END-TO-END AI AUTOMATION SYSTEMS.';
const SUBTEXT = 'We provide all-in-one AI automation services in one place.';

export function Hero() {
  const words = HEADLINE.split(' ');

  return (
    <section id="top" className="hero">
      <div className="hero__content">
        <h2 className="hero__heading">
          {words.map((word, i) => (
            <FadeUp key={`${word}-${i}`} as="span" y={32} delay={0.15 + i * 0.08}>
              {word}
            </FadeUp>
          ))}
        </h2>
        <FadeUp as="p" delay={0.9} className="hero__sub">
          {SUBTEXT}
        </FadeUp>
      </div>

      <FadeUp delay={1.3} className="scroll-hint" style={{ position: 'absolute' }}>
        <span>Scroll</span>
        <span className="scroll-hint__line" />
      </FadeUp>
    </section>
  );
}
