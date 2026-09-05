import { FadeUp } from '../components/FadeUp';
import { caseStudies } from '../content';

export function CaseStudies() {
  return (
    <section id="work" className="section">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">Case studies</span>
        </FadeUp>
        <FadeUp as="h2" className="h-section" delay={0.1}>
          Projects that delivered real results.
        </FadeUp>
        <FadeUp as="p" className="lead" delay={0.2}>
          Each project is a real solution to a real problem — designed, built, and deployed to save
          time and drive measurable business outcomes.
        </FadeUp>

        <div className="cases">
          {caseStudies.map((c, i) => (
            <FadeUp key={c.title} className="case" delay={0.06 * i}>
              <div className="case__head">
                <span className="card__index">{String(i + 1).padStart(2, '0')}</span>
                <h3 className="case__title">{c.title}</h3>
              </div>
              <dl className="case__meta">
                <div>
                  <dt>Problem</dt>
                  <dd>{c.problem}</dd>
                </div>
                <div>
                  <dt>Solution</dt>
                  <dd>{c.solution}</dd>
                </div>
                <div>
                  <dt>Outcome</dt>
                  <dd>{c.outcome}</dd>
                </div>
              </dl>
              <div className="case__foot">
                <div className="tags" style={{ marginTop: 0 }}>
                  {c.stack.map((s) => (
                    <span key={s} className="tag">
                      {s}
                    </span>
                  ))}
                </div>
                <a className="link-arrow" href={c.url} target="_blank" rel="noreferrer">
                  Watch case study →
                </a>
              </div>
            </FadeUp>
          ))}
        </div>
      </div>
    </section>
  );
}
