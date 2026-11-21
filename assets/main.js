// Mobil menyu
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Əlaqə forması: mesajı WhatsApp-da hazır açır
  var form = document.getElementById('wa-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements;
      var lines = [form.dataset.hello];
      [['name', '👤'], ['product', '📦'], ['qty', '#'], ['msg', '✎']].forEach(function (p) {
        var v = (f[p[0]].value || '').trim();
        if (v) lines.push(p[1] + ' ' + v);
      });
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
    });
  }
})();
