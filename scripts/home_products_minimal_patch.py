from pathlib import Path
import re

INDEX=Path('index.html')
html=INDEX.read_text(encoding='utf-8')

# Keep homepage product cards simple: front = image + name, flip = admin description.
section=re.compile(r'<section\s+class=["\']products-section[^>]*>.*?</section>',re.S|re.I)
products='''<section class="products-section section-padding" id="products">
<div class="container">
<div class="text-center mb-5"><span class="section-label">Our Products</span><h2 class="section-title">Digital Products We've <span class="gradient-text">Built</span></h2></div>
<div id="homeProductsGrid" class="products-grid-home"></div>
<div class="products-cta-home"><a href="products/" class="btn-outline-custom">Explore Products <i class="bi bi-arrow-right ms-2"></i></a></div>
</div></section>'''
html,n=section.subn(products,html,count=1)
if n!=1: raise SystemExit('Homepage Products section not found')

# Remove previous homepage product patch completely.
html=re.sub(r'<style id="hopix-home-minimal-products">.*?</script>','',html,flags=re.S)

addon='''
<style id="hopix-home-minimal-products">
.products-section .products-grid-home{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px;perspective:1400px}
.home-flip-card{height:380px;perspective:1200px;cursor:pointer}
.home-flip-inner{position:relative;width:100%;height:100%;transition:transform .75s cubic-bezier(.2,.75,.25,1);transform-style:preserve-3d}
.home-flip-card:hover .home-flip-inner{transform:rotateY(180deg)}
.home-flip-face{position:absolute;inset:0;border-radius:26px;overflow:hidden;backface-visibility:hidden;-webkit-backface-visibility:hidden;border:1px solid rgba(37,99,235,.12);box-shadow:0 18px 50px rgba(15,23,42,.11)}
.home-flip-front{background:linear-gradient(145deg,#edf5ff,#fff 55%,#eafaff);display:flex;align-items:center;justify-content:center}
.home-flip-front img{width:100%;height:100%;object-fit:cover;display:block}
.home-flip-front-name{position:absolute;left:18px;right:18px;bottom:18px;padding:20px 18px;border-radius:18px;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);font-size:clamp(1.5rem,2.5vw,2.1rem);line-height:1.15;font-weight:800;text-align:center;color:#0f172a;box-shadow:0 14px 35px rgba(15,23,42,.15)}
.home-flip-back{transform:rotateY(180deg);background:linear-gradient(145deg,#0f172a,#172554);color:#fff;padding:32px;display:flex;flex-direction:column;justify-content:center;text-align:center}
.home-flip-back .back-label{font-size:.7rem;letter-spacing:2px;text-transform:uppercase;opacity:.65;margin-bottom:12px}
.home-flip-back h3{font-size:1.45rem;font-weight:800;margin-bottom:15px}
.home-flip-back p{font-size:.88rem;line-height:1.75;color:rgba(255,255,255,.78);margin:0;display:-webkit-box;-webkit-line-clamp:8;-webkit-box-orient:vertical;overflow:hidden}
@media(max-width:991px){.products-section .products-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){.products-section .products-grid-home{grid-template-columns:1fr}.home-flip-card{height:340px}}
</style>
<script>
(function(){
const grid=document.getElementById('homeProductsGrid');if(!grid)return;
const API='https://zfgjhunmdpqzpmdnqtyv.supabase.co/rest/v1/products';
const KEY='sb_publishable_grTmssZ9sTu5YKXrH0ET6A_8wDNP2IT';
const esc=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
async function load(){try{const r=await fetch(API+'?select=name,image_url,description,status&status=eq.published&order=created_at.desc&limit=3',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});if(!r.ok)throw Error('Products request failed');const items=await r.json();if(!items.length){grid.innerHTML='<div class="products-empty-home">Our products are coming soon.</div>';return;}grid.innerHTML=items.map(p=>`<article class="home-flip-card"><div class="home-flip-inner"><div class="home-flip-face home-flip-front">${p.image_url?`<img src="${esc(p.image_url)}" alt="${esc(p.name||'HOPIX Product')}" loading="lazy">`:'<i class="bi bi-window-stack" style="font-size:70px;color:#94a3b8"></i>'}<div class="home-flip-front-name">${esc(p.name||'HOPIX Product')}</div></div><div class="home-flip-face home-flip-back"><div class="back-label">About this product</div><h3>${esc(p.name||'HOPIX Product')}</h3><p>${esc(p.description||'Product details will be available soon.')}</p></div></div></article>`).join('');}catch(e){console.warn('HOPIX homepage products',e)}}load();
})();
</script>'''
html=html.replace('</body>',addon+'\n</body>',1)
INDEX.write_text(html,encoding='utf-8')
