from urllib.request import urlopen

SRC = "https://raw.githubusercontent.com/mars0884-chu/baseball-GM/genealogy-form-v03-test/genealogy-form-v03/index.html"

with urlopen(SRC, timeout=30) as r:
    t = r.read().decode("utf-8")

# 版本與說明
for a, b in [
    ("族人簡易填報工具 v0.3", "族人簡易填報工具 v0.4"),
    ("第三版測試 v0.3", "第四版測試 v0.4"),
    ("行動填報工具 v0.3", "行動填報工具 v0.4"),
    ("簡易填報工具 v0.3", "簡易填報工具 v0.4"),
]:
    t = t.replace(a, b)

# 日期：現代日期可正規化；傳統年號原樣保留
t = t.replace(
    "出生日期（民國或西元皆可）",
    "出生日期／年代（民國、西元、年號皆可）",
)
t = t.replace(
    "例如：民國108年10月18日，或2019-10-18",
    "例如：民國108年10月18日、2019-10-18、1081018，或清光緒辛丑年",
)
t = t.replace(
    "不用換算；匯出時能辨識的日期會自動統一成民國格式。",
    "不用換算；能辨識的現代日期會自動統一成民國格式。像「清光緒辛丑年」這類年號文字會原樣保留，不自行改寫。",
)

# 已填人物清單提示
old_people_intro = '''<p>可以一次填自己、父母、配偶、子女或其他親人。每個人都是一張簡單卡片。</p>\n    <div id="peopleList"></div>'''
new_people_intro = '''<p>可以一次填自己、父母、配偶、子女或其他親人。每完成一人，都會留在下方清單，可隨時按「回去修改」。</p>\n    <div id="peopleCount" class="privacy card" style="margin:10px 0;padding:12px 14px"><strong>目前已填 0 人</strong><div class="small">新增下一人前，請先確認前面的人是否都在這裡。</div></div>\n    <div id="peopleList"></div>'''
if old_people_intro not in t:
    raise RuntimeError("找不到人物清單插入位置")
t = t.replace(old_people_intro, new_people_intro)

old_render = '''function renderPeople(){
  var box=$('peopleList');box.innerHTML='';
  if(!state.people.length){box.innerHTML='<p class="muted">還沒有新增人物。</p>';return}
  state.people.forEach(function(p,i){
    var d=document.createElement('div');d.className='person';
    var photoN=p.photos.length?'<span class="badge">照片 '+p.photos.length+'</span>':'';
    d.innerHTML='<div class="personHead"><div><div class="personName">'+escHtml(p.name)+'</div><div class="small">'+escHtml(p.rel)+'｜'+escHtml(p.gender)+'｜'+escHtml(p.life)+' '+photoN+'</div></div>'+
      '<div class="personBtns"><button class="ghost" data-edit="'+i+'">編輯</button><button class="danger" data-del="'+i+'">刪除</button></div></div>'+
      '<div class="small">父：'+escHtml(p.father||'未填')+'｜母：'+escHtml(p.mother||'未填')+'｜配偶：'+escHtml(p.spouse||'未填')+'</div>';
    box.appendChild(d);
  });
}'''
new_render = '''function renderPeople(){
  var box=$('peopleList');box.innerHTML='';
  var count=$('peopleCount');
  if(count){count.innerHTML='<strong>目前已填 '+state.people.length+' 人</strong><div class="small">'+(state.people.length?'下面每一位都可以按「回去修改」。':'還沒有新增人物。')+'</div>';}
  if(!state.people.length){box.innerHTML='<p class="muted">還沒有新增人物。</p>';return}
  state.people.forEach(function(p,i){
    var d=document.createElement('div');d.className='person';
    var photoN=p.photos.length?'<span class="badge">照片 '+p.photos.length+'</span>':'';
    d.innerHTML='<div class="personHead"><div><div class="personName">'+(i+1)+'. '+escHtml(p.name)+'</div><div class="small">'+escHtml(p.rel)+'｜'+escHtml(p.gender)+'｜'+escHtml(p.life)+' '+photoN+'</div></div>'+
      '<div class="personBtns"><button class="ghost" data-edit="'+i+'">回去修改</button><button class="danger" data-del="'+i+'">刪除</button></div></div>'+
      '<div class="small">父：'+escHtml(p.father||'未填')+'｜母：'+escHtml(p.mother||'未填')+'｜配偶：'+escHtml(p.spouse||'未填')+'</div>';
    box.appendChild(d);
  });
}'''
if old_render not in t:
    raise RuntimeError("找不到 renderPeople 函式")
t = t.replace(old_render, new_render)

old_norm = '''function normalizeDateInput(s){
  s=cleanName(s); if(!s)return '';
  var m=s.match(/^民國\\s*(\\d{1,3})\\s*[年\\-\\/.]\\s*(\\d{1,2})\\s*[月\\-\\/.]\\s*(\\d{1,2})\\s*日?$/);
  if(m)return '民國 '+parseInt(m[1],10)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日';
  m=s.match(/^(\\d{4})\\s*[\\-\\/.]\\s*(\\d{1,2})\\s*[\\-\\/.]\\s*(\\d{1,2})$/);
  if(m){var y=parseInt(m[1],10); if(y>=1912)return '民國 '+(y-1911)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日'; return s;}
  m=s.match(/^(\\d{1,3})\\s*[\\-\\/.]\\s*(\\d{1,2})\\s*[\\-\\/.]\\s*(\\d{1,2})$/);
  if(m)return '民國 '+parseInt(m[1],10)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日';
  return s;
}'''
new_norm = '''function normalizeDateInput(s){
  s=cleanName(s); if(!s)return '';
  var m=s.match(/^民國\\s*(\\d{1,3})\\s*[年\\-\\/.]\\s*(\\d{1,2})\\s*[月\\-\\/.]\\s*(\\d{1,2})\\s*日?$/);
  if(m)return '民國 '+parseInt(m[1],10)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日';
  m=s.match(/^(\\d{4})\\s*[\\-\\/.]\\s*(\\d{1,2})\\s*[\\-\\/.]\\s*(\\d{1,2})$/);
  if(m){var y=parseInt(m[1],10); if(y>=1912)return '民國 '+(y-1911)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日'; return s;}
  m=s.match(/^(\\d{1,3})\\s*[\\-\\/.]\\s*(\\d{1,2})\\s*[\\-\\/.]\\s*(\\d{1,2})$/);
  if(m)return '民國 '+parseInt(m[1],10)+' 年 '+pad(parseInt(m[2],10))+' 月 '+pad(parseInt(m[3],10))+' 日';
  m=s.match(/^(\\d{8})$/);
  if(m){var g=m[1],gy=parseInt(g.slice(0,4),10),gm=parseInt(g.slice(4,6),10),gd=parseInt(g.slice(6,8),10);if(gy>=1912&&gm>=1&&gm<=12&&gd>=1&&gd<=31)return '民國 '+(gy-1911)+' 年 '+pad(gm)+' 月 '+pad(gd)+' 日';}
  m=s.match(/^(?:民國\\s*)?(\\d{5,7})$/);
  if(m){var q=m[1],qy=parseInt(q.slice(0,-4),10),qm=parseInt(q.slice(-4,-2),10),qd=parseInt(q.slice(-2),10);if(qy>=1&&qy<=999&&qm>=1&&qm<=12&&qd>=1&&qd<=31)return '民國 '+qy+' 年 '+pad(qm)+' 月 '+pad(qd)+' 日';}
  return s;
}'''
if old_norm not in t:
    raise RuntimeError("找不到 normalizeDateInput 函式")
t = t.replace(old_norm, new_norm)

# 確認新 repo 的正式測試入口不再提 RawGitHack／Jotform
if "raw.githack" in t.lower() or "jotform" in t.lower():
    raise RuntimeError("輸出仍含第三方入口字樣")

with open("index.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(t)

print("built index.html", len(t), "chars")
