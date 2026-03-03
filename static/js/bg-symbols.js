(function () {
  var groups = [
    ['XIV','VII','IX','III','IV','XI','XL','LV','XLII','XXIV','MCM','CD',
     'VIII','XVII','XVIII','XCIX','LXIV','CXL','DCC','CCXL','MMXXV','XIII'],
    ['𓏺','𓎆','𓍢','𓆼','𓂭','𓆐','𓏺𓏺','𓎆𓏺','𓍢𓏺','𓆼𓆼','𓂭𓏺','𓎆𓎆','𓍢𓍢','𓏺𓎆','𓆐𓏺'],
    ['๗','๓','๙','๕','๘','๖','๔','๑','๑๒','๔๕','๗๗','๒๑','๓๓','๑๐','๙๙','๒๔','๑๕','๓๖'],
    ['42','99','256','365','512','108','7','21','33','77']
  ];
  var sizes = ['', '', 'bg-lg', 'bg-lg', 'bg-xl', 'bg-sm', 'bg-sm', 'bg-sm', 'bg-xs'];

  var COLS = 10;
  var ROWS = 12;
  var cellW = 100 / COLS;
  var cellH = 100 / ROWS;
  var gi = 0;

  var container = document.querySelector('.bg-symbols');
  if (!container) return;
  container.innerHTML = '';

  for (var r = 0; r < ROWS; r++) {
    for (var c = 0; c < COLS; c++) {
      var group = groups[gi % groups.length];
      gi++;

      var span = document.createElement('span');
      span.textContent = group[Math.floor(Math.random() * group.length)];

      var top = r * cellH + Math.random() * cellH * 0.7;
      var left = c * cellW + Math.random() * cellW * 0.7;
      span.style.top = top + '%';
      span.style.left = left + '%';
      span.style.rotate = (Math.random() * 60 - 30) + 'deg';

      var cls = sizes[Math.floor(Math.random() * sizes.length)];
      if (cls) span.className = cls;

      container.appendChild(span);
    }
  }
})();
