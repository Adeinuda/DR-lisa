import { site } from '../content';

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <div>
        <div style={{ color: '#fff', fontWeight: 700 }}>{site.name}</div>
        <div style={{ marginTop: 6 }}>{site.role} · Workflow Developer</div>
      </div>
      <span>© {year} {site.name}. All rights reserved.</span>
      <div style={{ display: 'flex', gap: 20 }}>
        <a href={site.linkedin} target="_blank" rel="noreferrer">
          LinkedIn
        </a>
        <a href={site.whatsapp} target="_blank" rel="noreferrer">
          WhatsApp
        </a>
        <a href={`mailto:${site.email}`}>Email</a>
      </div>
    </footer>
  );
}
