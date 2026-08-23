from pathlib import Path
import re

p = Path('index.html')
html = p.read_text(encoding='utf-8')

# Replace only the homepage products section.
section_re = re.compile(r'<section\s+class=["\']products-section[^>]*>.*?</section>', re.S | re.I)
new_section = '''<section class="products-section section-padding" id="products">
<div class="container">
<div class="text-center"><span class="section-label">Our Products</span><h2 class="section-title">Our <span class="gradient-text">Products</span></h2><p class="section-subtitle mx-auto">Explore the digital products built by HOPIX Tech Solutions.</p></div>
<div id="homeProductsGrid" class="products-grid-home" style="margin-top:40px"></div>
<div class="products-cta-home"><a href="products/" class="btn-primary-custom">Explore Products <i class="bi bi-arrow-right ms-2"></i></a></div>
</div></section>'''
html, count = section_re.subn(new_section, html, count=1)
if count != 1:
    raise SystemExit('Could not find homepage products section; refusing to modify index.html')

css = '''
<style id="hopix-final-products-css">
.products-section .products-grid-home{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px;perspective:1400px}
.products-section .product-card-home{position:relative!important;height:360px!important;padding:0!important;border-radius:26px!important;overflow:hidden!important;background:#fff!important;border:1px solid rgba(37,99,235,.14)!important;box-shadow:0 18px 50px rgba(15,23,42,.10)!important;transform-style:preserve-3d!important;transition:transform .25s ease,box-shadow .35s ease!important}
.products-section .product-card-home:hover{box-shadow:0 30px 75px rgba(37,99,235,.20)!important}
.hpx-home-img-wrap{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#edf5ff,#fff 55%,#e9f8ff);transform-style:preserve-3d}
.hpx-home-img{width:100%;height:100%;object-fit:cover;display:block;transform:translateZ(35px) scale(.94);transition:transform .4s ease;filter:drop-shadow(0 25px 25px rgba(15,23,42,.18))}
.product-card-home:hover .hpx-home-img{transform:translateZ(55px) scale(.98)}
.hpx-home-name{position:absolute;left:18px;right:18px;bottom:18px;padding:14px 16px;border-radius:16px;text-align:center;font-size:1.2rem;font-weight:800;color:#0f172a;background:rgba(255,255,255,.88);backdrop-filter:blur(12px);box-shadow:0 12px 30px rgba(15,23,42,.13);transform:translateZ(65px)}
.products-section .products-cta-home{text-align:center!important;margin-top:40px!important}
.products-section .products-cta-home a{text-decoration:none}
@media(max-width:991px){.products-section .products-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(max-width:650px){.products-section .products-grid-home{grid-template-columns:1fr!important}.products-section .product-card-home{height:330px!important}}
</style>
'''

js = '''
<script id="hopix-final-products-js">
(function(){
 const grid=document.getElementById('homeProductsGrid'); if(!grid)return;
 const API='https://zfgjhunmdpqzpmdnqtyv.supabase.co/rest/v1/products';
 const KEY='sb_publishable_grTmssZ9sTu5YKXrH0ET6A_8wDNP2IT';
 const esc=v=>String(v??'').replace(/[&<>\"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#039;'}[m]));
 async function load(){
  try{
   const r=await fetch(API+'?select=name,image_url,status&status=eq.published&order=created_at.desc&limit=3',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});
   if(!r.ok)throw new Error('products request failed');
   const items=await r.json();
   if(!items.length){grid.innerHTML='<div class="products-empty-home">Our products are coming soon.</div>';return;}
   grid.innerHTML=items.map(p=>`<article class="product-card-home"><div class="hpx-home-img-wrap">${p.image_url?`<img class="hpx-home-img" src="${esc(p.image_url)}" alt="${esc(p.name||'HOPIX Product')}" loading="lazy">`:'<i class="bi bi-window-stack" style="font-size:70px;color:#94a3b8"></i>'}<div class="hpx-home-name">${esc(p.name||'HOPIX Product')}</div></div></article>`).join('');
   grid.querySelectorAll('.product-card-home').forEach(card=>{
    card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.transform=`rotateX(${-y*7}deg) rotateY(${x*9}deg) translateY(-7px)`});
    card.addEventListener('pointerleave',()=>card.style.transform='');
   });
  }catch(e){console.error('HOPIX products:',e);grid.innerHTML='<div class="products-empty-home">Products are temporarily unavailable.</div>'}
 }
 load();
})();
</script>
'''

# Remove older homepage product patch blocks if present, then add one authoritative block.
html = re.sub(r'<style id="hopix-home-minimal-products">.*?</style>', '', html, flags=re.S)
html = re.sub(r'<script id="hopix-home-minimal-products">.*?</script>', '', html, flags=re.S)
html = re.sub(r'<style id="hopix-final-products-css">.*?</style>', '', html, flags=re.S)
html = re.sub(r'<script id="hopix-final-products-js">.*?</script>', '', html, flags=re.S)
html = html.replace('</head>', css + '</head>', 1)
html = html.replace('</body>', js + '</body>', 1)

# Restore the requested HOPIX logo animation if missing.
logo = '''
<style id="hopix-logo-animation">
.navbar-brand-custom{animation:hopixLogoEntrance 1.2s cubic-bezier(.22,1,.36,1) both}
.navbar-brand-custom span{display:inline-block;background-size:220% 100%;animation:hopixXFlow 2.4s .9s ease-in-out both}
@keyframes hopixLogoEntrance{0%{opacity:0;transform:translateY(-12px) scale(.94);letter-spacing:1px}55%{opacity:1;transform:translateY(2px) scale(1.01)}100%{opacity:1;transform:translateY(0) scale(1);letter-spacing:-.5px}}
@keyframes hopixXFlow{0%{background-position:0 50%}45%{background-position:100% 50%}100%{background-position:0 50%}}
</style>
'''
if 'id="hopix-logo-animation"' not in html:
    html = html.replace('</head>', logo + '</head>', 1)

p.write_text(html, encoding='utf-8')
