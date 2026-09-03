(function(){
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- dropdown nav: hover for pointer devices, click/keys for everyone --- */
  [].slice.call(document.querySelectorAll('.drop')).forEach(function(drop){
    var btn = drop.querySelector(':scope > button.mtop');
    if (!btn) return;
    function close(){ drop.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }
    btn.addEventListener('click', function(e){
      e.preventDefault();
      var open = drop.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    if (window.matchMedia('(hover:hover)').matches){
      drop.addEventListener('mouseenter', function(){ drop.classList.add('open'); btn.setAttribute('aria-expanded','true'); });
      drop.addEventListener('mouseleave', close);
    }
    document.addEventListener('click', function(e){ if(!drop.contains(e.target)) close(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });
  });
  /* panel stays reachable with the keyboard even if JS never ran */
  var st = document.createElement('style');
  st.textContent = '.drop:focus-within .panel{display:grid!important}';
  document.head.appendChild(st);

  /* --- mobile drawer --- */
  var burger = document.getElementById('burger'), mob = document.getElementById('mobnav');
  if (burger && mob){
    burger.addEventListener('click', function(){
      var on = mob.classList.toggle('on');
      burger.setAttribute('aria-expanded', on ? 'true' : 'false');
      burger.setAttribute('aria-label', on ? 'Close menu' : 'Open menu');
    });
    mob.addEventListener('click', function(e){
      if (e.target.tagName === 'A'){ mob.classList.remove('on'); burger.setAttribute('aria-expanded','false'); }
    });
  }

  /* --- the pipe run lights the band you are reading --- */
  /* on the collated single page the bands sit inside a route wrapper, so match both depths */
  var secs = [].slice.call(document.querySelectorAll('main > section[id], main > section.opsec[id] > section[id]'));
  if (!reduce && secs.length && 'IntersectionObserver' in window){
    var so = new IntersectionObserver(function(ents){
      ents.forEach(function(en){ en.target.classList.toggle('is-live', en.isIntersecting && en.intersectionRatio > 0.3); });
    }, {threshold:[0,0.3,0.6]});
    secs.forEach(function(el){ so.observe(el); });
  }

  /* --- reveal --- */
  var rvs = [].slice.call(document.querySelectorAll('.rv'));
  if (reduce || !('IntersectionObserver' in window)){ rvs.forEach(function(el){ el.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function(ents){
      ents.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.06});
    rvs.forEach(function(el){ io.observe(el); });
  }

  /* --- guide filter (DIY hub) --- */
  var chips = [].slice.call(document.querySelectorAll('[data-filter]'));
  if (chips.length){
    var cards = [].slice.call(document.querySelectorAll('[data-cat]'));
    chips.forEach(function(chip){
      chip.addEventListener('click', function(){
        var want = chip.getAttribute('data-filter');
        chips.forEach(function(c){
          var on = c === chip;
          c.classList.toggle('on', on);
          c.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        var shown = 0;
        cards.forEach(function(card){
          var ok = want === 'all' || card.getAttribute('data-cat') === want;
          card.hidden = !ok;
          if (ok) shown++;
        });
        var count = document.getElementById('gcount');
        if (count) count.textContent = shown === cards.length ? cards.length + ' guides' : shown + ' of ' + cards.length + ' guides';
      });
    });
    /* a #category link from the nav lands on the matching filter */
    var want = (location.hash || '').replace('#', '');
    if (want) {
      var hit = chips.filter(function(c){ return c.id === want; })[0];
      if (hit) { hit.click(); if (hit.closest('.filters')) hit.scrollIntoView({block:'center'}); }
    }
  }

  /* --- hot-linked image fallback: show the labelled placeholder if an asset 404s --- */
  [].slice.call(document.querySelectorAll('.ph img')).forEach(function(img){
    function flag(){ var p = img.closest('.ph'); if (p) p.classList.add('missing'); }
    if (img.complete && img.naturalWidth === 0) flag();
    img.addEventListener('error', flag);
    img.addEventListener('load', function(){ if (img.naturalWidth === 0) flag(); });
  });

  /* --- booking form: validate client-side, then the mailto client delivers --- */
  [].slice.call(document.querySelectorAll('form.book')).forEach(function(form){
    form.addEventListener('submit', function(e){
      var bad = false;
      [].slice.call(form.querySelectorAll('[required]')).forEach(function(f){
        var wrap = f.closest('.field'), ok = f.value.trim().length > 0;
        if (ok && f.type === 'email') ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f.value.trim());
        if (ok && f.type === 'tel') ok = f.value.replace(/[^0-9]/g,'').length >= 7;
        if (wrap) wrap.classList.toggle('err', !ok);
        f.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad){ bad = true; f.focus(); }
      });
      if (bad) e.preventDefault();
    });
    [].slice.call(form.querySelectorAll('input,select,textarea')).forEach(function(f){
      f.addEventListener('input', function(){ var w = f.closest('.field'); if (w) w.classList.remove('err'); });
    });
  });

  /* --- accordion (FAQ) --- */
  [].slice.call(document.querySelectorAll('.faq details > summary')).forEach(function(s){})();

  /* --- sticky mobile bar steps aside over the form --- */
  var mbar = document.querySelector('.mbar'), target = document.getElementById('book');
  if (mbar && target && 'IntersectionObserver' in window){
    new IntersectionObserver(function(ents){
      ents.forEach(function(en){
        mbar.style.transition = 'transform .25s ease';
        mbar.style.transform = en.isIntersecting ? 'translateY(120%)' : 'translateY(0)';
      });
    }, {threshold:0.06}).observe(target);
  }
})();
