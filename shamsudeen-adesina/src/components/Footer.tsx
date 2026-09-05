export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="footer">
      <span>© {year} Shamsudeen Adesina</span>
      <span>AI Automation Engineer</span>
      <div style={{ display: 'flex', gap: 20 }}>
        <a href="https://www.linkedin.com" target="_blank" rel="noreferrer">
          LinkedIn
        </a>
        <a href="https://x.com" target="_blank" rel="noreferrer">
          X
        </a>
        <a href="https://github.com" target="_blank" rel="noreferrer">
          GitHub
        </a>
      </div>
    </footer>
  );
}
