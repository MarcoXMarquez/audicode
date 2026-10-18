// static/js/fileHandler.js

/**
 * File attachment and upload handling
 */

import uiModule from './ui.js';
import spinnerModule from './spinner.js';

let pendingFiles = [];
let uploaded = [];
// Holds the full meta (id/name/mime/size/width/height/…) from the most recent
// uploadPending() so callers can stamp width/height onto their attachment
// objects without changing uploadPending()'s return signature.
let _lastUploadedMeta = [];
let API_BASE = '';
let _uploadSpinners = [];
let _uploadAbortCtrl = null;
let _uploading = false;
let _lastUploadCancelled = false;
const _previewUrls = new WeakMap();

const MAX_FILES = 10;
const MAX_VISIBLE = 3;
let _expanded = false;

function _getPreviewUrl(f) {
  if (!f) return '';
  let url = _previewUrls.get(f);
  if (!url) {
    url = URL.createObjectURL(f);
    _previewUrls.set(f, url);
  }
  return url;
}

function _revokePreviewUrl(f) {
  const url = _previewUrls.get(f);
  if (url) {
    try { URL.revokeObjectURL(url); } catch (_) {}
    _previewUrls.delete(f);
  }
}

/**
 * Initialize with dependencies
 */
export function init(apiBase) {
  API_BASE = apiBase;
  initPasteAndDropHandlers();
}

/**
 * Handle clipboard paste events on composer:
 * - Detects screenshots/images and converts them into file attachments
 * - Detects long text (> 12 lines or > 600 chars) and converts it into a snippet chip
 */
export function handlePasteEvent(e) {
  if (!e.clipboardData) return;

  // 1. Check for clipboard images (screenshots, copied images)
  const items = e.clipboardData.items;
  if (items && items.length > 0) {
    for (let i = 0; i < items.length; i++) {
      const item = items[i];
      if (item.type && item.type.startsWith('image/')) {
        const blob = item.getAsFile();
        if (blob) {
          e.preventDefault();
          const d = new Date();
          const pad = (n) => String(n).padStart(2, '0');
          const timestamp = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
          const ext = blob.type.split('/')[1] || 'png';
          const file = new File([blob], `screenshot_${timestamp}.${ext}`, { type: blob.type || 'image/png' });
          addFiles([file]);
          _showToast('Captura de pantalla adjuntada');
          return;
        }
      }
    }
  }

  // 2. Check for long pasted text (> 12 lines OR > 600 characters)
  const text = e.clipboardData.getData('text');
  if (text) {
    const lines = text.split(/\r\n|\r|\n/);
    const lineCount = lines.length;
    const charCount = text.length;

    if (lineCount > 12 || charCount > 600) {
      e.preventDefault();
      const d = new Date();
      const pad = (n) => String(n).padStart(2, '0');
      const timeStr = `${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
      const fileName = `pasted_text_${timeStr}.txt`;

      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const file = new File([blob], fileName, { type: 'text/plain' });
      file._isPastedSnippet = true;
      file._lineCount = lineCount;
      file._charCount = charCount;
      file._previewText = text.slice(0, 200).trim();

      addFiles([file]);
      _showToast(`Texto largo adjuntado (${lineCount} líneas)`);
      return;
    }
  }
}

/**
 * Initialize paste and drag-drop handlers on composer
 */
export function initPasteAndDropHandlers() {
  const wire = () => {
    const msg = document.getElementById('message');
    if (!msg || msg._audiPasteWired) return;
    msg._audiPasteWired = true;

    msg.addEventListener('paste', handlePasteEvent);

    msg.addEventListener('dragover', (e) => {
      e.preventDefault();
      msg.classList.add('drag-active');
    });
    msg.addEventListener('dragleave', () => msg.classList.remove('drag-active'));
    msg.addEventListener('drop', (e) => {
      msg.classList.remove('drag-active');
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        e.preventDefault();
        addFiles(Array.from(e.dataTransfer.files));
      }
    });
  };

  wire();
  setTimeout(wire, 200);
  setTimeout(wire, 800);
  document.addEventListener('DOMContentLoaded', wire);
}

/**
 * Open file picker dialog
 */
export function openPicker() {
  document.getElementById('file-input').click();
}

/**
 * Render the attachment strip with pending files.
 * 1-3 files: show individual chips.
 * 4+  files: collapse into a single "N files" badge (click to expand).
 */
export function renderAttachStrip() {
  const strip = document.getElementById('attach-strip');

  while (strip.firstChild) strip.removeChild(strip.firstChild);
  if (pendingFiles.length === 0) {
    _expanded = false;
    if (window._updateSendBtnIcon) window._updateSendBtnIcon();
    return;
  }

  const total = pendingFiles.length;
  const collapsed = total > MAX_VISIBLE && !_expanded;

  if (collapsed) {
    // Single compact badge: "5 files ×"
    const badge = document.createElement('div');
    badge.className = 'thumb thumb-collapsed';
    const label = document.createElement('span');
    label.textContent = total + ' file' + (total > 1 ? 's' : '');
    label.className = 'thumb-collapsed-label';
    badge.appendChild(label);
    badge.title = pendingFiles.map(f => f.name || 'pasted-image').join('\n');
    badge.style.cursor = 'pointer';
    badge.addEventListener('click', (e) => {
      if (e.target.closest('.thumb-collapsed-x')) return;
      _expanded = true;
      renderAttachStrip();
    });
    const x = document.createElement('button');
    x.className = 'thumb-collapsed-x';
    x.textContent = '\u00d7';
    x.title = 'Remove all';
    x.addEventListener('click', (e) => { e.stopPropagation(); clearPending(); });
    badge.appendChild(x);
    strip.appendChild(badge);
  } else {
    // Show individual chips
    for (let idx = 0; idx < total; idx++) {
      strip.appendChild(_createChip(pendingFiles[idx], idx));
    }
  }
  if (window._updateSendBtnIcon) window._updateSendBtnIcon();
}

function _createChip(f, idx) {
  const chip = document.createElement('div');
  chip.className = 'thumb';

  // Render compact snippet pill if text was pasted
  if (f._isPastedSnippet) {
    chip.classList.add('thumb-snippet');
    chip.title = f._previewText ? `Vista previa:\n${f._previewText}...` : `Snippet de texto (${f._lineCount} líneas)`;

    const iconSpan = document.createElement('span');
    iconSpan.className = 'thumb-snippet-icon';
    iconSpan.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>';
    chip.appendChild(iconSpan);

    const span = document.createElement('span');
    span.className = 'thumb-snippet-label';
    span.innerHTML = `Texto pegado <span class="thumb-snippet-lines">(${f._lineCount} líneas)</span>`;
    chip.appendChild(span);

    const x = document.createElement('button');
    x.textContent = '\u00d7';
    x.setAttribute('aria-label', 'Eliminar snippet');
    x.addEventListener('click', (e) => { e.stopPropagation(); removePending(idx); });
    chip.appendChild(x);
    return chip;
  }

  const isImage = f.type?.startsWith('image/') || /\.(png|jpg|jpeg|gif|webp|svg|bmp)$/i.test(f.name || '');
  if (isImage) {
    chip.classList.add('thumb-image');  // lets CSS overlay the remove-X on the corner (mobile)
    const img = document.createElement('img');
    img.className = 'thumb-img';
    img.src = _getPreviewUrl(f);
    img.alt = f.name || 'image';
    chip.appendChild(img);
  } else {
    chip.classList.add('thumb-doc');
    const ext = (f.name || '').split('.').pop().toUpperCase();
    if (ext && ext.length <= 4 && ext !== f.name) {
      const badge = document.createElement('span');
      badge.className = 'thumb-doc-badge';
      badge.textContent = ext;
      chip.appendChild(badge);
    }
    const span = document.createElement('span');
    span.textContent = f.name || 'document';
    chip.appendChild(span);
  }
  const x = document.createElement('button');
  x.textContent = '\u00d7';
  x.setAttribute('aria-label', 'Remove attachment');
  x.addEventListener('click', (e) => { e.stopPropagation(); removePending(idx); });
  chip.appendChild(x);
  return chip;
}

/**
 * Remove a pending file by index
 */
export function removePending(idx) {
  if (_uploading) cancelUpload();
  _revokePreviewUrl(pendingFiles[idx]);
  pendingFiles.splice(idx, 1);
  renderAttachStrip();
}

/**
 * Upload all pending files to server
 */
export async function uploadPending(opts = {}) {
  if (pendingFiles.length === 0) return [];
  _lastUploadCancelled = false;

  // The message bubble is shown immediately, but the upload can take a moment —
  // dim the chips and overlay a whirlpool so it's clear the files are still
  // being sent (and aren't stuck). Cleared in the finally below.
  const strip = document.getElementById('attach-strip');
  if (strip) {
    strip.classList.add('attach-uploading');
    // Put a whirlpool ON each attachment chip (image/doc) so the spinner sits on
    // the thing being uploaded, not floating over the whole strip.
    strip.querySelectorAll('.thumb').forEach(chip => {
      try {
        const sp = spinnerModule.create('', 'clean', 'whirlpool');
        const ov = document.createElement('span');
        ov.className = 'thumb-upload-spinner';
        ov.appendChild(sp.createElement());
        chip.appendChild(ov);
        sp.start();
        _uploadSpinners.push(sp);
      } catch (_) { /* spinner is best-effort */ }
    });
  }

  const fd = new FormData();
  pendingFiles.forEach(f => fd.append('files', f, f.name || 'paste.png'));
  if (opts.sessionId) fd.append('session_id', opts.sessionId);
  _uploadAbortCtrl = new AbortController();
  _uploading = true;
  const timeoutId = setTimeout(() => {
    if (_uploadAbortCtrl && !_uploadAbortCtrl.signal.aborted) {
      try { _uploadAbortCtrl.abort(); } catch (_) {}
    }
  }, 120000);

  try {
    const res = await fetch(`${API_BASE}/api/upload`, {
      method: 'POST',
      body: fd,
      signal: _uploadAbortCtrl.signal,
    });
    if (!res.ok) {
      // Surface the failure instead of swallowing it. Previously a non-OK
      // response (e.g. 429 rate limit, 413 too large) was ignored: the files
      // silently vanished and the chat sent with no attachments, so the model
      // "didn't even see them" (issue #1346). Show the server's reason and keep
      // pendingFiles so the strip re-renders for a retry (see finally below).
      let detail = '';
      try { const e = await res.json(); detail = e.detail || e.error || ''; } catch (_) {}
      _showToast('Upload failed' + (detail ? ': ' + detail : ` (HTTP ${res.status})`));
      return [];
    }
    const data = await res.json();
    uploaded = (data.files || []);
    if (uploaded.some(x => x && x.gallery_id)) {
      try { localStorage.setItem('gallery-fresh-chat-upload', String(Date.now())); } catch (_) {}
      window.dispatchEvent(new CustomEvent('gallery-refresh', { detail: { source: 'chat-upload' } }));
    }
    pendingFiles = [];          // clear only on success
    // Stash the full meta (incl. width/height for images) on the module so
    // callers that want it can grab it via getLastUploadedMeta(). Keep the
    // returned shape as `ids` for backward-compatibility with existing call sites.
    _lastUploadedMeta = uploaded;
    return uploaded.map(x => x.id);
  } catch (e) {
    if (e && e.name === 'AbortError') {
      _lastUploadCancelled = true;
      _showToast('Upload cancelled');
      return [];
    }
    _showToast('Upload failed: ' + (e?.message || 'network error'));
    return [];
  } finally {
    clearTimeout(timeoutId);
    _uploading = false;
    _uploadAbortCtrl = null;
    _uploadSpinners.forEach(sp => { try { sp.stop && sp.stop(); } catch (_) {} });
    _uploadSpinners = [];
    if (strip) strip.classList.remove('attach-uploading');
    // Re-render: empty on success (chips gone), or restored on error so the
    // user can retry — and either way the spinners are removed.
    renderAttachStrip();
  }
}

/**
 * Add files to pending list (capped at MAX_FILES)
 */
export function addFiles(files) {
  for (const f of files) {
    if (pendingFiles.length >= MAX_FILES) {
      _showToast(`Max ${MAX_FILES} files allowed`);
      break;
    }
    pendingFiles.push(f);
  }
  renderAttachStrip();
}

function _showToast(msg) {
  if (window.showToast) { window.showToast(msg); return; }
  // Fallback inline toast
  let t = document.getElementById('_attach-toast');
  if (!t) {
    t = document.createElement('div');
    t.id = '_attach-toast';
    t.style.cssText = 'position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:var(--panel);border:1px solid var(--red);color:var(--red);padding:6px 14px;border-radius:6px;font-size:13px;z-index:9999;opacity:0;transition:opacity .3s';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.style.opacity = '0'; }, 2500);
}

/**
 * Get pending files count
 */
export function getPendingCount() {
  return pendingFiles.length;
}

/**
 * Get raw pending File objects (for reading content before upload clears them)
 */
export function getPendingRaw() {
  return [...pendingFiles];
}

/**
 * Get pending file metadata (name, size, type) for display
 */
export function getPendingInfo() {
  return pendingFiles.map(f => {
    const isImage = f.type?.startsWith('image/') || /\.(png|jpg|jpeg|gif|webp|svg|bmp)$/i.test(f.name || '');
    return {
      name: f.name || 'pasted-image',
      size: f.size || 0,
      mime: f.type || '',
      previewUrl: isImage ? _getPreviewUrl(f) : '',
    };
  });
}

/**
 * Clear all pending files
 */
export function clearPending() {
  if (_uploading) cancelUpload();
  pendingFiles.forEach(_revokePreviewUrl);
  pendingFiles = [];
  renderAttachStrip();
}

/** Full meta (incl. width/height for images) from the most recent uploadPending(). */
export function getLastUploadedMeta() {
  return _lastUploadedMeta;
}

export function isUploading() {
  return _uploading;
}

export function wasLastUploadCancelled() {
  return _lastUploadCancelled;
}

export function cancelUpload() {
  _lastUploadCancelled = true;
  if (_uploadAbortCtrl && !_uploadAbortCtrl.signal.aborted) {
    try { _uploadAbortCtrl.abort(); } catch (_) {}
  }
}

var escapeHtml = uiModule.esc;

const fileHandlerModule = {
  init,
  openPicker,
  renderAttachStrip,
  removePending,
  uploadPending,
  addFiles,
  getPendingCount,
  getPendingInfo,
  getPendingRaw,
  clearPending,
  getLastUploadedMeta,
  isUploading,
  wasLastUploadCancelled,
  cancelUpload,
};

export default fileHandlerModule;
