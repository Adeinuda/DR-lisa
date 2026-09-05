import { marqueeItems } from '../content';

export function Marquee() {
  const doubled = [...marqueeItems, ...marqueeItems];
  return (
    <div className="marquee" aria-hidden="true">
      <div className="marquee__track">
        {doubled.map((item, i) => (
          <span key={i} className="marquee__item">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
