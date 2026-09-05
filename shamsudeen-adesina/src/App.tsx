import { BackgroundVideo } from './components/BackgroundVideo';
import { Nav } from './components/Nav';
import { Footer } from './components/Footer';
import { Hero } from './sections/Hero';
import { Marquee } from './sections/Marquee';
import { Services } from './sections/Services';
import { Tools } from './sections/Tools';
import { CaseStudies } from './sections/CaseStudies';
import { Process } from './sections/Process';
import { About } from './sections/About';
import { Testimonials } from './sections/Testimonials';
import { Contact } from './sections/Contact';

export default function App() {
  return (
    <>
      <BackgroundVideo />
      <Nav />
      <main className="page">
        <Hero />
        <Marquee />
        <Services />
        <Tools />
        <CaseStudies />
        <Process />
        <About />
        <Testimonials />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
