from pathlib import Path
import re

p = Path('index.html')
html = p.read_text(encoding='utf-8')

# Idempotent: do not add the social block twice.
if 'id="hopix-footer-socials"' not in html:
    css = '''
/* HOPIX footer social links */
#hopix-footer-socials{display:flex;align-items:center;gap:10px;margin-top:18px;flex-wrap:wrap}
#hopix-footer-socials a{width:38px;height:38px;border:1px solid rgba(255,255,255,.12);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:rgba(255,255,255,.72);font-size:16px;text-decoration:none;transition:all .3s ease;background:rgba(255,255,255,.035)}
#hopix-footer-socials a:hover{color:#fff;background:linear-gradient(135deg,#2563eb,#06b6d4);border-color:transparent;transform:translateY(-3px);box-shadow:0 8px 20px rgba(37,99,235,.25)}
@media(max-width:575px){#hopix-footer-socials{justify-content:center}}
'''
    html = html.replace('</style>', css + '</style>', 1)

    social = '''
<div id="hopix-footer-socials" aria-label="HOPIX social media links">
  <a href="https://www.instagram.com/hopix_01/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" title="Instagram"><i class="bi bi-instagram"></i></a>
  <a href="#" aria-label="LinkedIn" title="LinkedIn"><i class="bi bi-linkedin"></i></a>
  <a href="#" aria-label="Facebook" title="Facebook"><i class="bi bi-facebook"></i></a>
  <a href="#" aria-label="YouTube" title="YouTube"><i class="bi bi-youtube"></i></a>
  <a href="#" aria-label="X" title="X"><i class="bi bi-twitter-x"></i></a>
  <a href="#" aria-label="WhatsApp" title="WhatsApp"><i class="bi bi-whatsapp"></i></a>
</div>
'''

    # Put social icons below the footer description, without disturbing the existing footer layout.
    footer_desc = re.search(r'(<p[^>]*class=["\']footer-desc["\'][^>]*>.*?</p>)', html, re.S | re.I)
    if footer_desc:
        pos = footer_desc.end()
        html = html[:pos] + social + html[pos:]
    else:
        # Fallback: place them in the footer before the bottom bar.
        marker = re.search(r'(<div[^>]*class=["\']footer-bottom["\'][^>]*>)', html, re.S | re.I)
        if not marker:
            raise SystemExit('Could not locate footer insertion point; refusing to modify index.html')
        html = html[:marker.start()] + social + html[marker.start():]

    p.write_text(html, encoding='utf-8')
