import { motion } from 'framer-motion';
import { site } from '../content';

const links = [
  { href: '#services', label: 'Services' },
  { href: '#work', label: 'Work' },
  { href: '#process', label: 'Process' },
  { href: '#about', label: 'About' },
];

export function Nav() {
  return (
    <motion.nav
      className="nav"
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay: 0.1, ease: [0.22, 1, 0.36, 1] }}
    >
      <a href="#top" className="nav__brand">
        {site.name}
      </a>
      <div className="nav__links">
        {links.map((l) => (
          <a key={l.href} href={l.href}>
            {l.label}
          </a>
        ))}
        <a href={site.bookingUrl} target="_blank" rel="noreferrer" className="nav__cta">
          Book a call
        </a>
      </div>
    </motion.nav>
  );
}
