import { FadeUp } from '../components/FadeUp';
import { site, skills } from '../content';

export function About() {
  return (
    <section id="about" className="section">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">About</span>
        </FadeUp>

        <div className="about">
          <div>
            <FadeUp as="h2" className="about__name" delay={0.1}>
              Shamsudeen
              <br />
              Adesina
            </FadeUp>
            <FadeUp as="p" className="about__role" delay={0.2}>
              {site.role} · Workflow Developer
            </FadeUp>
            <FadeUp className="about__portrait" delay={0.3}>
              <img src={site.portrait} alt="Shamsudeen Adesina" loading="lazy" />
            </FadeUp>
          </div>

          <div className="about__body">
            <FadeUp as="p" delay={0.15}>
              I focus on building practical AI systems that help businesses automate operations,
              reduce repetitive tasks, and improve customer interactions through intelligent
              workflows and AI-powered systems.
            </FadeUp>
            <FadeUp as="p" delay={0.25}>
              I'm not here to sell complexity — I'm here to solve real problems. Whether you need a
              chatbot that actually works, a workflow that runs itself, or a CRM that sells while you
              sleep — I build it.
            </FadeUp>
            <FadeUp as="p" delay={0.32}>
              Building intelligent systems that work while you don't have to.
            </FadeUp>

            <FadeUp className="tags" delay={0.4}>
              {skills.map((t) => (
                <span key={t} className="tag">
                  {t}
                </span>
              ))}
            </FadeUp>

            <FadeUp className="btn-row" delay={0.45} style={{ marginTop: 32 }}>
              <a className="btn btn--ghost" href={site.projectsUrl} target="_blank" rel="noreferrer">
                View all projects
              </a>
              <a className="btn btn--ghost" href={site.linkedin} target="_blank" rel="noreferrer">
                LinkedIn
              </a>
            </FadeUp>
          </div>
        </div>
      </div>
    </section>
  );
}
