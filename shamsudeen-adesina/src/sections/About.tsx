import { FadeUp } from '../components/FadeUp';

const tags = [
  'Python',
  'TypeScript',
  'n8n',
  'Make',
  'Zapier',
  'OpenAI',
  'Anthropic',
  'LangChain',
  'Supabase',
  'Postgres',
  'Vector DBs',
  'Twilio',
  'HubSpot',
  'Airtable',
];

export function About() {
  return (
    <section id="about" className="section">
      <div className="section__inner">
        <FadeUp>
          <span className="eyebrow">The engineer</span>
        </FadeUp>

        <div className="about">
          <FadeUp as="h2" className="about__name" delay={0.1}>
            Shamsudeen
            <br />
            Adesina
          </FadeUp>

          <div className="about__body">
            <FadeUp as="p" delay={0.15}>
              I am an AI automation engineer. I help founders and operations teams replace slow,
              manual, error-prone work with systems that run on their own — quietly, reliably,
              and at scale.
            </FadeUp>
            <FadeUp as="p" delay={0.25}>
              I have spent years inside the plumbing of businesses: CRMs, spreadsheets, inboxes,
              support desks and databases. That is where the real leverage lives, and that is where
              I build. Every system I ship is designed to be understood, monitored and extended by
              the people who use it.
            </FadeUp>
            <FadeUp as="p" delay={0.35}>
              No bloated retainers. No black boxes. Just end-to-end automation that pays for itself.
            </FadeUp>

            <FadeUp className="tags" delay={0.4}>
              {tags.map((t) => (
                <span key={t} className="tag">
                  {t}
                </span>
              ))}
            </FadeUp>
          </div>
        </div>
      </div>
    </section>
  );
}
