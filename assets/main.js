document.documentElement.classList.add('js');
// Menu mobile
const burger = document.querySelector('.burger');
const menu = document.querySelector('nav ul');
if (burger) burger.addEventListener('click', () => menu.classList.toggle('open'));
document.querySelectorAll('nav ul a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));

// Apparition au défilement
const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: .12 }) : null;
document.querySelectorAll('.reveal').forEach(el => io ? io.observe(el) : el.classList.add('in'));

// Texte tapé dans le hero
const role = document.querySelector('[data-roles]');
if (role && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const roles = JSON.parse(role.dataset.roles);
  const out = role.querySelector('.txt');
  let r = 0, i = 0, del = false;
  (function tick() {
    const w = roles[r];
    out.textContent = w.slice(0, i);
    if (!del && i === w.length) { del = true; return setTimeout(tick, 1800); }
    if (del && i === 0) { del = false; r = (r + 1) % roles.length; }
    i += del ? -1 : 1;
    setTimeout(tick, del ? 35 : 70);
  })();
}

// Filtres des write-ups
document.querySelectorAll('.filters button').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.filters button').forEach(x => x.classList.toggle('on', x === b));
  const f = b.dataset.f;
  document.querySelectorAll('#ctf .card').forEach(c => {
    c.style.display = f === 'all' || c.dataset.tags.includes(f) ? '' : 'none';
  });
}));

// Lien actif dans la navigation
const links = [...document.querySelectorAll('nav ul a[href^="#"]')];
if (links.length && io) {
  const spy = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id));
  }), { rootMargin: '-45% 0px -50% 0px' });
  links.forEach(a => { const s = document.querySelector(a.getAttribute('href')); if (s) spy.observe(s); });
}
