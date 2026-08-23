from pathlib import Path
import re

INDEX = Path('index.html')
html = INDEX.read_text(encoding='utf-8')

# Always restore the HOPIX navbar logo animation. The old version only added it
# when absent, so later homepage patches could silently leave the logo static.
logo_css = '''
/* HOPIX premium logo animation */
.navbar-brand-custom{position:relative;display:inline-block;transform-origin:left center;animation:hopixLogoEntrance 1.2s cubic-bezier(.22,1,.36,1) both}
.navbar-brand-custom span{display:inline-block;position:relative;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;background-size:220% 100%;animation:hopixXFlow 2.4s .9s ease-in-out both}
.navbar-brand-custom:after{content:'';position:absolute;left:0;bottom:-6px;width:0;height:2px;border-radius:999px;background:var(--gradient);animation:hopixUnderline .9s 1.15s cubic-bezier(.22,1,.36,1) forwards}
.navbar-brand-custom:before{content:'';position:absolute;top:2px;bottom:2px;left:-8px;width:4px;border-radius:999px;background:rgba(255,255,255,.95);opacity:0;transform:translateX(-8px) skewX(-14deg);pointer-events:none;animation:hopixLightSweep 1s 1.25s ease-out forwards}
.navbar-brand-custom:hover{transform:translateY(-1px) scale(1.02)}
@keyframes hopixLogoEntrance{0%{opacity:0;transform:translateY(-12px) scale(.94);letter-spacing:1px}55%{opacity:1;transform:translateY(2px) scale(1.01);letter-spacing:-.5px}100%{opacity:1;transform:translateY(0) scale(1);letter-spacing:-.5px}}
@keyframes hopixXFlow{0%{background-position:0 50%}45%{background-position:100% 50%}100%{background-position:0 50%}}
@keyframes hopixUnderline{from{width:0}to{width:32px}}
@keyframes hopixLightSweep{0%{opacity:0;transform:translateX(-8px) skewX(-14deg)}18%{opacity:.95}100%{opacity:0;transform:translateX(55px) skewX(-14deg)}}
@media(prefers-reduced-motion:reduce){.navbar-brand-custom,.navbar-brand-custom span,.navbar-brand-custom:before,.navbar-brand-custom:after{animation:none;opacity:1;transform:none}}
'''

# Remove any previous copy, then inject exactly one fresh copy.
html = re.sub(r'/\* HOPIX premium logo animation \*/.*?@media\(prefers-reduced-motion:reduce\)\{.*?\}\n?', '', html, flags=re.S)
html = html.replace('</style>', logo_css + '\n</style>', 1)

# Replace ONLY the homepage Products section.
section = re.compile(r'<section\s+class=["\']products-section[^>]*>.*?</section>', re.S | re.I)
products = '''<section class="products-section section-padding" id="products">
  <div class="container">
    <div class="text-center mb-5">
      <span class="section-label">Our Products</span>
      <h2 class="section-title">Digital Products We've <span class="gradient-text">Built</span></h2>
      <p class="section-subtitle mx-auto">Explore real-world web applications and digital products created by HOPIX Tech Solutions.</p>
    </div>
    <div id="homeProductsGrid" class="products-grid-home mt-5"></div>
    <div class="products-cta-home">
      <a href="products/" class="btn-outline-custom">Explore Products <i class="bi bi-arrow-right ms-2"></i></a>
    </div>
  </div>
</section>'''
html, n = section.subn(products, html, count=1)
if n != 1:
    raise SystemExit('Homepage Products section was not found; no homepage changes were made.')

addon = '''
<style id="hopix-home-minimal-products">
.products-section .products-grid-home{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px;perspective:1400px}
.products-section .product-card-home{position:relative;height:365px;border-radius:28px;overflow:hidden;background:#fff;border:1px solid rgba(37,99,235,.12);box-shadow:0 18px 50px rgba(15,23,42,.10);transform-style:preserve-3d;transition:transform .25s ease,box-shadow .35s ease;cursor:default}
.products-section .product-card-home:hover{box-shadow:0 30px 75px rgba(37,99,235,.20)}
.home-minimal-image-wrap{position:absolute;inset:0;background:linear-gradient(145deg,#edf5ff,#f9fcff 55%,#e9f8ff);display:flex;align-items:center;justify-content:center;transform-style:preserve-3d}
.home-minimal-image{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;transform:translateZ(28px) scale(.94);filter:drop-shadow(0 25px 25px rgba(15,23,42,.18));transition:transform .45s ease}
.products-section .product-card-home:hover .home-minimal-image{transform:translateZ(42px) scale(.98)}
.home-minimal-name{position:absolute;left:20px;right:20px;bottom:20px;z-index:5;padding:15px 18px;border-radius:17px;background:rgba(255,255,255,.86);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.9);box-shadow:0 12px 30px rgba(15,23,42,.12);font-size:1.2rem;font-weight:800;text-align:center;color:#0f172a;transform:translateZ(55px);transition:.3s}
.products-section .product-card-home:hover .home-minimal-name{transform:translateZ(72px) translateY(-4px)}
.products-section .products-cta-home{margin-top:42px;text-align:center}
@media(max-width:991px){.products-section .products-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){.products-section .products-grid-home{grid-template-columns:1fr;gap:22px}.products-section .product-card-home{height:330px}}
</style>
<script>
(function(){
 const grid=document.getElementById('homeProductsGrid'); if(!grid)return;
 const API='https://zfgjhunmdpqzpmdnqtyv.supabase.co/rest/v1/products';
 const KEY='sb_publishable_grTmssZ9sTu5YKXrH0ET6A_8wDNP2IT';
 const esc=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
 async function load(){
  try{
   const r=await fetch(API+'?select=name,image_url,status&status=eq.published&order=created_at.desc&limit=3',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});
   if(!r.ok)throw Error('Products request failed');
   const items=await r.json();
   if(!items.length){grid.innerHTML='<div class="products-empty-home">Our products are coming soon.</div>';return;}
   grid.innerHTML=items.map(p=>`<article class="product-card-home"><div class="home-minimal-image-wrap">${p.image_url?`<img class="home-minimal-image" src="${esc(p.image_url)}" alt="${esc(p.name||'HOPIX Product')}" loading="lazy">`:'<i class="bi bi-window-stack" style="font-size:70px;color:#94a3b8"></i>'}<div class="home-minimal-name">${esc(p.name||'HOPIX Product')}</div></div></article>`).join('');
   grid.querySelectorAll('.product-card-home').forEach(card=>{
    card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.transform=`rotateX(${-y*7}deg) rotateY(${x*9}deg) translateY(-7px)`});
    card.addEventListener('pointerleave',()=>card.style.transform='');
   });
  }catch(e){console.warn('HOPIX homepage products',e)}
 }
 load();
})();
</script>'''

# Replace previous minimal addon if present, otherwise append once.
html = re.sub(r'<style id="hopix-home-minimal-products">.*?</script>', '', html, flags=re.S)
html = html.replace('</body>', addon + '\n</body>', 1)
INDEX.write_text(html, encoding='utf-8')
