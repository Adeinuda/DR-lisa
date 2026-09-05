import { BackgroundVideo } from './components/BackgroundVideo';
import { Nav } from './components/Nav';
import { Footer } from './components/Footer';
import { Hero } from './sections/Hero';
import { Marquee } from './sections/Marquee';
import { Services } from './sections/Services';
import { Process } from './sections/Process';
import { About } from './sections/About';
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
        <Process />
        <About />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
