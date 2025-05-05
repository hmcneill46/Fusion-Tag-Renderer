// Theme menu logic
const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('theme-menu');
hamburger.addEventListener('click', () => menu.classList.toggle('show'));
document.querySelectorAll('#theme-menu button').forEach(btn => btn.addEventListener('click', () => {
  document.body.className = btn.dataset.theme;
  localStorage.setItem('theme', btn.dataset.theme);
  menu.classList.remove('show');
}));
document.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('theme'); if (saved) document.body.className = saved;
  const rawData = document.getElementById('filters-data').value;
  const fname = document.getElementById('filters-filename-hidden').value;
  if (rawData) loadAndPreviewTagsFromRaw(rawData, fname);
  autoResizeTextarea('filenames-textarea');
});

// Dropzones
function makeDropzone(zoneId, inputId, textId, filenameHiddenId) {
  const zone = document.getElementById(zoneId);
  const input = document.getElementById(inputId);
  const text = document.getElementById(textId);
  const hiddenName = filenameHiddenId ? document.getElementById(filenameHiddenId) : null;
  zone.addEventListener('click', () => input.click());
  input.addEventListener('change', () => {
    if (input.files.length) {
      text.textContent = input.files[0].name;
      if (hiddenName) hiddenName.value = input.files[0].name;
      if (inputId === 'filters-input') loadAndPreviewTags(input.files[0]);
      if (inputId === 'files-input') loadFilenames(input.files[0]);
    }
  });
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', e => { e.preventDefault(); zone.classList.remove('dragover'); });
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      input.files = e.dataTransfer.files;
      text.textContent = e.dataTransfer.files[0].name;
      if (hiddenName) hiddenName.value = e.dataTransfer.files[0].name;
      if (inputId === 'filters-input') loadAndPreviewTags(e.dataTransfer.files[0]);
      if (inputId === 'files-input') loadFilenames(e.dataTransfer.files[0]);
    }
  });
}
makeDropzone('filters-zone','filters-input','filters-text','filters-filename-hidden');
makeDropzone('files-zone','files-input','files-text');

// Auto-resize textarea
function autoResizeTextarea(id) {
  const ta = document.getElementById(id);
  if (!ta) return;
  const resize = () => { ta.style.height = 'auto'; ta.style.height = ta.scrollHeight + 'px'; };
  ta.addEventListener('input', resize);
  resize();
}

// Preview tags
function loadAndPreviewTags(file) {
  const reader = new FileReader();
  reader.onload = e => loadAndPreviewTagsFromRaw(e.target.result, file.name);
  reader.readAsText(file);
}
function loadAndPreviewTagsFromRaw(raw, fname) {
  try {
    const data = JSON.parse(raw); const list = data.filters || [];
    const container = document.getElementById('available-tags'); container.innerHTML = '';
    list.filter(f => f.isEnabled).forEach(f => {
      const tag = document.createElement('div'); tag.className='filter-tag';
      tag.style.backgroundColor=f.tagColor||'#333'; tag.style.color=f.textColor||'#fff'; tag.title=f.name;
      if(f.imageURL){const img=document.createElement('img');img.src=f.imageURL;img.className='filter-icon';img.alt=f.name;tag.appendChild(img);} else tag.textContent=f.name;
      container.appendChild(tag);
    });
    document.getElementById('available-tags-preview').style.display='block';
    document.getElementById('filters-text').textContent=fname;
  } catch(err){console.error('Invalid JSON',err);} }

// Load filenames into textarea immediately
function loadFilenames(file) {
  const reader = new FileReader();
  reader.onload = e => {
    const text = e.target.result;
    const ta = document.getElementById('filenames-textarea');
    ta.value = text;
    autoResizeTextarea('filenames-textarea');
  };
  reader.readAsText(file);
}
