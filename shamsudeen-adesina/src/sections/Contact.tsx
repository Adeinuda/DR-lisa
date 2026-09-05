import { FadeUp } from '../components/FadeUp';

const EMAIL = 'hello@shamsudeenadesina.com';

export function Contact() {
  return (
    <section id="contact" className="cta">
      <div className="section__inner" style={{ width: '100%' }}>
        <FadeUp>
          <span className="eyebrow">Let's build</span>
        </FadeUp>
        <FadeUp as="h2" className="cta__title" delay={0.1}>
          Automate
          <br />
          the boring.
          <br />
          Scale the rest.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.25}>
          Tell me what is slowing your team down. I will reply within one business day with a
          plan for what we can automate first.
        </FadeUp>
        <FadeUp className="btn-row" delay={0.35}>
          <a className="btn btn--solid" href={`mailto:${EMAIL}`}>
            Start a project →
          </a>
          <a className="btn btn--ghost" href="https://cal.com" target="_blank" rel="noreferrer">
            Book a call
          </a>
        </FadeUp>
      </div>
    </section>
  );
}
