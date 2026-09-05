import { FadeUp } from '../components/FadeUp';
import { site } from '../content';

export function Contact() {
  return (
    <section id="contact" className="cta">
      <div className="section__inner" style={{ width: '100%' }}>
        <FadeUp>
          <span className="eyebrow">Let's build</span>
        </FadeUp>
        <FadeUp as="h2" className="cta__title" delay={0.1}>
          Ready to
          <br />
          automate the
          <br />
          repetitive?
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.25}>
          Let's build an AI automation system tailored to your business — one that runs 24/7,
          scales with you, and frees your team to focus on growth.
        </FadeUp>
        <FadeUp className="btn-row" delay={0.35}>
          <a className="btn btn--solid" href={site.bookingUrl} target="_blank" rel="noreferrer">
            Schedule a call →
          </a>
          <a className="btn btn--ghost" href={site.whatsapp} target="_blank" rel="noreferrer">
            WhatsApp
          </a>
          <a className="btn btn--ghost" href={`mailto:${site.email}`}>
            {site.email}
          </a>
        </FadeUp>
      </div>
    </section>
  );
}
