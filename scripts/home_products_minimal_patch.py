from pathlib import Path

INDEX = Path('index.html')
MARK = '/* HOPIX HOME PRODUCTS MINIMAL V2 */'

html = INDEX.read_text(encoding='utf-8')

css = r'''
<style>
/* HOPIX HOME PRODUCTS MINIMAL V2 */
.products-section .products-grid-home{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px;perspective:1400px;align-items:stretch}
.products-section .product-card-home{position:relative;height:365px;border-radius:28px;overflow:hidden;background:#fff;border:1px solid rgba(37,99,235,.12);box-shadow:0 18px 50px rgba(15,23,42,.10);transform-style:preserve-3d;transition:transform .25s ease,box-shadow .35s ease,border-color .35s ease;cursor:pointer}
.products-section .product-card-home:hover{box-shadow:0 30px 75px rgba(37,99,235,.20);border-color:rgba(37,99,235,.28)}
.products-section .product-card-home:before{content:'';position:absolute;inset:0;z-index:4;pointer-events:none;border-radius:28px;background:linear-gradient(125deg,rgba(255,255,255,.42),transparent 30%,transparent 65%,rgba(37,99,235,.12));opacity:.55}
.home-minimal-image{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;transform:translateZ(28px) scale(.94);filter:drop-shadow(0 25px 25px rgba(15,23,42,.18));transition:transform .45s ease,filter .45s ease}
.products-section .product-card-home:hover .home-minimal-image{transform:translateZ(42px) scale(.98);filter:drop-shadow(0 35px 30px rgba(15,23,42,.24))}
.home-minimal-image-wrap{position:absolute;inset:0;background:linear-gradient(145deg,#edf5ff 0%,#f9fcff 55%,#e9f8ff 100%);display:flex;align-items:center;justify-content:center;transform-style:preserve-3d}
.home-minimal-image-wrap:after{content:'';position:absolute;left:10%;right:10%;bottom:28px;height:30px;background:rgba(15,23,42,.12);filter:blur(20px);border-radius:50%;transform:translateZ(-15px)}
.home-minimal-name{position:absolute;left:20px;right:20px;bottom:20px;z-index:6;padding:15px 18px;border-radius:17px;background:rgba(255,255,255,.84);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.9);box-shadow:0 12px 30px rgba(15,23,42,.12);font-size:1.18rem;font-weight:800;line-height:1.25;text-align:center;color:#0f172a;text-shadow:0 2px 10px rgba(37,99,235,.14);transform:translateZ(55px);transition:.3s}
.products-section .product-card-home:hover .home-minimal-name{transform:translateZ(72px) translateY(-4px);box-shadow:0 18px 38px rgba(37,99,235,.18)}
.products-section .product-card-home .product-content-home,.products-section .product-card-home .product-category-home,.products-section .product-card-home .product-link-home{display:none!important}
.products-section .products-cta-home{margin-top:42px}
.products-section .products-cta-home .btn-outline-custom{padding:13px 28px;border-color:rgba(37,99,235,.24);background:#fff;box-shadow:0 10px 28px rgba(37,99,235,.10)}
@media(max-width:991px){.products-section .products-grid-home{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){.products-section .products-grid-home{grid-template-columns:1fr;gap:22px}.products-section .product-card-home{height:330px}}
</style>
'''

js = r'''
<script>
/* HOPIX HOME PRODUCTS MINIMAL JS V2 */
(function(){
 const grid=document.getElementById('homeProductsGrid');
 if(!grid)return;
 const API='https://zfgjhunmdpqzpmdnqtyv.supabase.co/rest/v1/products';
 const KEY='sb_publishable_grTmssZ9sTu5YKXrH0ET6A_8wDNP2IT';
 const esc=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
 function bind3D(){
   grid.querySelectorAll('.product-card-home').forEach(card=>{
     if(card.dataset.minimal3d)return;
     card.dataset.minimal3d='1';
     card.addEventListener('pointermove',e=>{
       const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
       card.style.transform=`rotateX(${-y*7}deg) rotateY(${x*9}deg) translateY(-7px)`;
     });
     card.addEventListener('pointerleave',()=>card.style.transform='');
   });
 }
 function render(items){
   if(!items.length){grid.innerHTML='<div class="products-empty-home">Our products are coming soon.</div>';return;}
   grid.innerHTML=items.map(p=>{
     const name=p.name||p.product_name||'HOPIX Product';
     const image=p.image_url||p.main_image_url||p.image||'';
     return `<article class="product-card-home" aria-label="${esc(name)}"><div class="home-minimal-image-wrap">${image?`<img class="home-minimal-image" src="${esc(image)}" alt="${esc(name)}" loading="lazy">`:'<i class="bi bi-window-stack" style="font-size:70px;color:#94a3b8;transform:translateZ(30px)"></i>'}<div class="home-minimal-name">${esc(name)}</div></div></article>`;
   }).join('');
   bind3D();
 }
 async function load(){
   try{
     const r=await fetch(API+'?select=*&status=eq.published&order=created_at.desc&limit=3',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});
     if(!r.ok)throw new Error('products request failed');
     render(await r.json());
   }catch(e){console.warn('Minimal homepage products:',e);}
 }
 const cta=document.querySelector('.products-cta-home a');
 if(cta){cta.href='products/';cta.textContent='Explore Products';}
 ['homeProductModal','hpxHomeModal'].forEach(id=>{const el=document.getElementById(id);if(el)el.remove();});
 load();
})();
</script>
'''

if MARK not in html:
    html = html.replace('</head>', css + '\n</head>', 1)
    html = html.replace('</body>', js + '\n</body>', 1)

INDEX.write_text(html, encoding='utf-8')
