import{R as j,r as B,m as e,n as b,o as xe,p as ne,q as pe,s as _,t as Q}from"./index-BFMhCHYa.js";let he={data:""},ge=t=>typeof window=="object"?((t?t.querySelector("#_goober"):window._goober)||Object.assign((t||document.head).appendChild(document.createElement("style")),{innerHTML:" ",id:"_goober"})).firstChild:t||he,me=/(?:([\u0080-\uFFFF\w-%@]+) *:? *([^{;]+?);|([^;}{]*?) *{)|(}\s*)/g,ve=/\/\*[^]*?\*\/|  +/g,X=/\n+/g,N=(t,s)=>{let o="",r="",u="";for(let l in t){let c=t[l];l[0]=="@"?l[1]=="i"?o=l+" "+c+";":r+=l[1]=="f"?N(c,l):l+"{"+N(c,l[1]=="k"?"":s)+"}":typeof c=="object"?r+=N(c,s?s.replace(/([^,])+/g,f=>l.replace(/([^,]*:\S+\([^)]*\))|([^,])+/g,d=>/&/.test(d)?d.replace(/&/g,f):f?f+" "+d:d)):l):c!=null&&(l=/^--/.test(l)?l:l.replace(/[A-Z]/g,"-$&").toLowerCase(),u+=N.p?N.p(l,c):l+":"+c+";")}return o+(s&&u?s+"{"+u+"}":u)+r},S={},re=t=>{if(typeof t=="object"){let s="";for(let o in t)s+=o+re(t[o]);return s}return t},je=(t,s,o,r,u)=>{let l=re(t),c=S[l]||(S[l]=(d=>{let x=0,n=11;for(;x<d.length;)n=101*n+d.charCodeAt(x++)>>>0;return"go"+n})(l));if(!S[c]){let d=l!==t?t:(x=>{let n,a,i=[{}];for(;n=me.exec(x.replace(ve,""));)n[4]?i.shift():n[3]?(a=n[3].replace(X," ").trim(),i.unshift(i[0][a]=i[0][a]||{})):i[0][n[1]]=n[2].replace(X," ").trim();return i[0]})(t);S[c]=N(u?{["@keyframes "+c]:d}:d,o?"":"."+c)}let f=o&&S.g?S.g:null;return o&&(S.g=S[c]),((d,x,n,a)=>{a?x.data=x.data.replace(a,d):x.data.indexOf(d)===-1&&(x.data=n?d+x.data:x.data+d)})(S[c],s,r,f),c},ye=(t,s,o)=>t.reduce((r,u,l)=>{let c=s[l];if(c&&c.call){let f=c(o),d=f&&f.props&&f.props.className||/^go/.test(f)&&f;c=d?"."+d:f&&typeof f=="object"?f.props?"":N(f,""):f===!1?"":f}return r+u+(c??"")},"");function E(t){let s=this||{},o=t.call?t(s.p):t;return je(o.unshift?o.raw?ye(o,[].slice.call(arguments,1),s.p):o.reduce((r,u)=>Object.assign(r,u&&u.call?u(s.p):u),{}):o,ge(s.target),s.g,s.o,s.k)}E.bind({g:1});E.bind({k:1});const $e=t=>{try{const s=localStorage.getItem(t);return typeof s=="string"?JSON.parse(s):void 0}catch{return}};function P(t,s){const[o,r]=j.useState();j.useEffect(()=>{const l=$e(t);r(typeof l>"u"||l===null?typeof s=="function"?s():s:l)},[s,t]);const u=j.useCallback(l=>{r(c=>{let f=l;typeof l=="function"&&(f=l(c));try{localStorage.setItem(t,JSON.stringify(f))}catch{}return f})},[t]);return[o,u]}const be=typeof window>"u";function V(t){const s={pending:"yellow",success:"green",error:"red",notFound:"purple",redirected:"gray"};return t.isFetching&&t.status==="success"?t.isFetching==="beforeLoad"?"purple":"blue":s[t.status]}function ke(t,s){const o=t.find(r=>r.routeId===s.id);return o?V(o):"gray"}function oe(){const[t,s]=j.useState(!1);return j[be?"useEffect":"useLayoutEffect"](()=>{s(!0)},[]),t}const Ce=t=>{const s=Object.getOwnPropertyNames(Object(t)),o=typeof t=="bigint"?`${t.toString()}n`:t;try{return JSON.stringify(o,s)}catch{return"unable to stringify"}};function ee(t){const s=oe(),[o,r]=j.useState(t),u=j.useCallback(l=>{we(()=>{s&&r(l)})},[s]);return[o,u]}function we(t){Promise.resolve().then(t).catch(s=>setTimeout(()=>{throw s}))}function ze(t,s=[o=>o]){return t.map((o,r)=>[o,r]).sort(([o,r],[u,l])=>{for(const c of s){const f=c(o),d=c(u);if(typeof f>"u"){if(typeof d>"u")continue;return 1}if(f!==d)return f>d?1:-1}return r-l}).map(([o])=>o)}const v={colors:{inherit:"inherit",current:"currentColor",transparent:"transparent",black:"#000000",white:"#ffffff",neutral:{50:"#f9fafb",100:"#f2f4f7",200:"#eaecf0",300:"#d0d5dd",400:"#98a2b3",500:"#667085",600:"#475467",700:"#344054",800:"#1d2939",900:"#101828"},darkGray:{50:"#525c7a",100:"#49536e",200:"#414962",300:"#394056",400:"#313749",500:"#292e3d",600:"#212530",700:"#191c24",800:"#111318",900:"#0b0d10"},gray:{50:"#f9fafb",100:"#f2f4f7",200:"#eaecf0",300:"#d0d5dd",400:"#98a2b3",500:"#667085",600:"#475467",700:"#344054",800:"#1d2939",900:"#101828"},blue:{25:"#F5FAFF",50:"#EFF8FF",100:"#D1E9FF",200:"#B2DDFF",300:"#84CAFF",400:"#53B1FD",500:"#2E90FA",600:"#1570EF",700:"#175CD3",800:"#1849A9",900:"#194185"},green:{25:"#F6FEF9",50:"#ECFDF3",100:"#D1FADF",200:"#A6F4C5",300:"#6CE9A6",400:"#32D583",500:"#12B76A",600:"#039855",700:"#027A48",800:"#05603A",900:"#054F31"},red:{50:"#fef2f2",100:"#fee2e2",200:"#fecaca",300:"#fca5a5",400:"#f87171",500:"#ef4444",600:"#dc2626",700:"#b91c1c",800:"#991b1b",900:"#7f1d1d",950:"#450a0a"},yellow:{25:"#FFFCF5",50:"#FFFAEB",100:"#FEF0C7",200:"#FEDF89",300:"#FEC84B",400:"#FDB022",500:"#F79009",600:"#DC6803",700:"#B54708",800:"#93370D",900:"#7A2E0E"},purple:{25:"#FAFAFF",50:"#F4F3FF",100:"#EBE9FE",200:"#D9D6FE",300:"#BDB4FE",400:"#9B8AFB",500:"#7A5AF8",600:"#6938EF",700:"#5925DC",800:"#4A1FB8",900:"#3E1C96"},teal:{25:"#F6FEFC",50:"#F0FDF9",100:"#CCFBEF",200:"#99F6E0",300:"#5FE9D0",400:"#2ED3B7",500:"#15B79E",600:"#0E9384",700:"#107569",800:"#125D56",900:"#134E48"},pink:{25:"#fdf2f8",50:"#fce7f3",100:"#fbcfe8",200:"#f9a8d4",300:"#f472b6",400:"#ec4899",500:"#db2777",600:"#be185d",700:"#9d174d",800:"#831843",900:"#500724"},cyan:{25:"#ecfeff",50:"#cffafe",100:"#a5f3fc",200:"#67e8f9",300:"#22d3ee",400:"#06b6d4",500:"#0891b2",600:"#0e7490",700:"#155e75",800:"#164e63",900:"#083344"}},alpha:{100:"ff",90:"e5",80:"cc",70:"b3",60:"99",50:"80",40:"66",30:"4d",20:"33",10:"1a",0:"00"},font:{size:{"2xs":"calc(var(--tsrd-font-size) * 0.625)",xs:"calc(var(--tsrd-font-size) * 0.75)",sm:"calc(var(--tsrd-font-size) * 0.875)",md:"var(--tsrd-font-size)",lg:"calc(var(--tsrd-font-size) * 1.125)",xl:"calc(var(--tsrd-font-size) * 1.25)","2xl":"calc(var(--tsrd-font-size) * 1.5)","3xl":"calc(var(--tsrd-font-size) * 1.875)","4xl":"calc(var(--tsrd-font-size) * 2.25)","5xl":"calc(var(--tsrd-font-size) * 3)","6xl":"calc(var(--tsrd-font-size) * 3.75)","7xl":"calc(var(--tsrd-font-size) * 4.5)","8xl":"calc(var(--tsrd-font-size) * 6)","9xl":"calc(var(--tsrd-font-size) * 8)"},lineHeight:{"3xs":"calc(var(--tsrd-font-size) * 0.75)","2xs":"calc(var(--tsrd-font-size) * 0.875)",xs:"calc(var(--tsrd-font-size) * 1)",sm:"calc(var(--tsrd-font-size) * 1.25)",md:"calc(var(--tsrd-font-size) * 1.5)",lg:"calc(var(--tsrd-font-size) * 1.75)",xl:"calc(var(--tsrd-font-size) * 2)","2xl":"calc(var(--tsrd-font-size) * 2.25)","3xl":"calc(var(--tsrd-font-size) * 2.5)","4xl":"calc(var(--tsrd-font-size) * 2.75)","5xl":"calc(var(--tsrd-font-size) * 3)","6xl":"calc(var(--tsrd-font-size) * 3.25)","7xl":"calc(var(--tsrd-font-size) * 3.5)","8xl":"calc(var(--tsrd-font-size) * 3.75)","9xl":"calc(var(--tsrd-font-size) * 4)"},weight:{thin:"100",extralight:"200",light:"300",normal:"400",medium:"500",semibold:"600",bold:"700",extrabold:"800",black:"900"},fontFamily:{sans:"ui-sans-serif, Inter, system-ui, sans-serif, sans-serif",mono:"ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"}},breakpoints:{xs:"320px",sm:"640px",md:"768px",lg:"1024px",xl:"1280px","2xl":"1536px"},border:{radius:{none:"0px",xs:"calc(var(--tsrd-font-size) * 0.125)",sm:"calc(var(--tsrd-font-size) * 0.25)",md:"calc(var(--tsrd-font-size) * 0.375)",lg:"calc(var(--tsrd-font-size) * 0.5)",xl:"calc(var(--tsrd-font-size) * 0.75)","2xl":"calc(var(--tsrd-font-size) * 1)","3xl":"calc(var(--tsrd-font-size) * 1.5)",full:"9999px"}},size:{0:"0px",.25:"calc(var(--tsrd-font-size) * 0.0625)",.5:"calc(var(--tsrd-font-size) * 0.125)",1:"calc(var(--tsrd-font-size) * 0.25)",1.5:"calc(var(--tsrd-font-size) * 0.375)",2:"calc(var(--tsrd-font-size) * 0.5)",2.5:"calc(var(--tsrd-font-size) * 0.625)",3:"calc(var(--tsrd-font-size) * 0.75)",3.5:"calc(var(--tsrd-font-size) * 0.875)",4:"calc(var(--tsrd-font-size) * 1)",4.5:"calc(var(--tsrd-font-size) * 1.125)",5:"calc(var(--tsrd-font-size) * 1.25)",5.5:"calc(var(--tsrd-font-size) * 1.375)",6:"calc(var(--tsrd-font-size) * 1.5)",6.5:"calc(var(--tsrd-font-size) * 1.625)",7:"calc(var(--tsrd-font-size) * 1.75)",8:"calc(var(--tsrd-font-size) * 2)",9:"calc(var(--tsrd-font-size) * 2.25)",10:"calc(var(--tsrd-font-size) * 2.5)",11:"calc(var(--tsrd-font-size) * 2.75)",12:"calc(var(--tsrd-font-size) * 3)",14:"calc(var(--tsrd-font-size) * 3.5)",16:"calc(var(--tsrd-font-size) * 4)",20:"calc(var(--tsrd-font-size) * 5)",24:"calc(var(--tsrd-font-size) * 6)",28:"calc(var(--tsrd-font-size) * 7)",32:"calc(var(--tsrd-font-size) * 8)",36:"calc(var(--tsrd-font-size) * 9)",40:"calc(var(--tsrd-font-size) * 10)",44:"calc(var(--tsrd-font-size) * 11)",48:"calc(var(--tsrd-font-size) * 12)",52:"calc(var(--tsrd-font-size) * 13)",56:"calc(var(--tsrd-font-size) * 14)",60:"calc(var(--tsrd-font-size) * 15)",64:"calc(var(--tsrd-font-size) * 16)",72:"calc(var(--tsrd-font-size) * 18)",80:"calc(var(--tsrd-font-size) * 20)",96:"calc(var(--tsrd-font-size) * 24)"},shadow:{xs:(t="rgb(0 0 0 / 0.1)")=>"0 1px 2px 0 rgb(0 0 0 / 0.05)",sm:(t="rgb(0 0 0 / 0.1)")=>`0 1px 3px 0 ${t}, 0 1px 2px -1px ${t}`,md:(t="rgb(0 0 0 / 0.1)")=>`0 4px 6px -1px ${t}, 0 2px 4px -2px ${t}`,lg:(t="rgb(0 0 0 / 0.1)")=>`0 10px 15px -3px ${t}, 0 4px 6px -4px ${t}`,xl:(t="rgb(0 0 0 / 0.1)")=>`0 20px 25px -5px ${t}, 0 8px 10px -6px ${t}`,"2xl":(t="rgb(0 0 0 / 0.25)")=>`0 25px 50px -12px ${t}`,inner:(t="rgb(0 0 0 / 0.05)")=>`inset 0 2px 4px 0 ${t}`,none:()=>"none"},zIndices:{hide:-1,auto:"auto",base:0,docked:10,dropdown:1e3,sticky:1100,banner:1200,overlay:1300,modal:1400,popover:1500,skipLink:1600,toast:1700,tooltip:1800}},G=j.createContext(void 0),J=j.createContext(void 0),Fe=()=>{const t=j.useContext(J);if(!t)throw new Error("useDevtoolsOnClose must be used within a TanStackRouterDevtools component");return t},te=({expanded:t,style:s={}})=>{const o=ie();return e.jsx("span",{className:o.expander,children:e.jsx("svg",{xmlns:"http://www.w3.org/2000/svg",width:"12",height:"12",fill:"none",viewBox:"0 0 24 24",className:b(o.expanderIcon(t)),children:e.jsx("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"2",d:"M9 18l6-6-6-6"})})})};function Se(t,s){if(s<1)return[];let o=0;const r=[];for(;o<t.length;)r.push(t.slice(o,o+s)),o=o+s;return r}const Re=({handleEntry:t,label:s,value:o,subEntries:r=[],subEntryPages:u=[],type:l,expanded:c=!1,toggleExpanded:f,pageSize:d,renderer:x})=>{const[n,a]=B.useState([]),[i,g]=B.useState(void 0),p=ie(),k=()=>{g(o())};return e.jsx("div",{className:p.entry,children:u.length?e.jsxs(e.Fragment,{children:[e.jsxs("button",{className:p.expandButton,onClick:()=>f(),children:[e.jsx(te,{expanded:c}),s,e.jsxs("span",{className:p.info,children:[String(l).toLowerCase()==="iterable"?"(Iterable) ":"",r.length," ",r.length>1?"items":"item"]})]}),c?u.length===1?e.jsx("div",{className:p.subEntries,children:r.map((C,m)=>t(C))}):e.jsx("div",{className:p.subEntries,children:u.map((C,m)=>e.jsx("div",{children:e.jsxs("div",{className:p.entry,children:[e.jsxs("button",{className:b(p.labelButton,"labelButton"),onClick:()=>a(w=>w.includes(m)?w.filter(U=>U!==m):[...w,m]),children:[e.jsx(te,{expanded:n.includes(m)})," ","[",m*d," ..."," ",m*d+d-1,"]"]}),n.includes(m)?e.jsx("div",{className:p.subEntries,children:C.map(w=>t(w))}):null]})},m))}):null]}):l==="function"?e.jsx(e.Fragment,{children:e.jsx(M,{renderer:x,label:e.jsxs("button",{onClick:k,className:p.refreshValueBtn,children:[e.jsx("span",{children:s})," 🔄"," "]}),value:i,defaultExpanded:{}})}):e.jsxs(e.Fragment,{children:[e.jsxs("span",{children:[s,":"]})," ",e.jsx("span",{className:p.value,children:Ce(o)})]})})};function Ne(t){return Symbol.iterator in t}function M({value:t,defaultExpanded:s,renderer:o=Re,pageSize:r=100,filterSubEntries:u,...l}){const[c,f]=B.useState(!!s),d=B.useCallback(()=>f(g=>!g),[]);let x=typeof t,n=[];const a=g=>{const p=s===!0?{[g.label]:!0}:s==null?void 0:s[g.label];return{...g,defaultExpanded:p}};Array.isArray(t)?(x="array",n=t.map((g,p)=>a({label:p.toString(),value:g}))):t!==null&&typeof t=="object"&&Ne(t)&&typeof t[Symbol.iterator]=="function"?(x="Iterable",n=Array.from(t,(g,p)=>a({label:p.toString(),value:g}))):typeof t=="object"&&t!==null&&(x="object",n=Object.entries(t).map(([g,p])=>a({label:g,value:p}))),n=u?u(n):n;const i=Se(n,r);return o({handleEntry:g=>e.jsx(M,{value:t,renderer:o,filterSubEntries:u,...l,...g},g.label),type:x,subEntries:n,subEntryPages:i,value:t,expanded:c,toggleExpanded:d,pageSize:r,...l})}const Ue=t=>{const{colors:s,font:o,size:r,alpha:u,shadow:l,border:c}=v,{fontFamily:f,lineHeight:d,size:x}=o,n=t?E.bind({target:t}):E;return{entry:n`
      font-family: ${f.mono};
      font-size: ${x.xs};
      line-height: ${d.sm};
      outline: none;
      word-break: break-word;
    `,labelButton:n`
      cursor: pointer;
      color: inherit;
      font: inherit;
      outline: inherit;
      background: transparent;
      border: none;
      padding: 0;
    `,expander:n`
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: ${r[3]};
      height: ${r[3]};
      padding-left: 3px;
      box-sizing: content-box;
    `,expanderIcon:a=>a?n`
          transform: rotate(90deg);
          transition: transform 0.1s ease;
        `:n`
        transform: rotate(0deg);
        transition: transform 0.1s ease;
      `,expandButton:n`
      display: flex;
      gap: ${r[1]};
      align-items: center;
      cursor: pointer;
      color: inherit;
      font: inherit;
      outline: inherit;
      background: transparent;
      border: none;
      padding: 0;
    `,value:n`
      color: ${s.purple[400]};
    `,subEntries:n`
      margin-left: ${r[2]};
      padding-left: ${r[2]};
      border-left: 2px solid ${s.darkGray[400]};
    `,info:n`
      color: ${s.gray[500]};
      font-size: ${x["2xs"]};
      padding-left: ${r[1]};
    `,refreshValueBtn:n`
      appearance: none;
      border: 0;
      cursor: pointer;
      background: transparent;
      color: inherit;
      padding: 0;
      font-family: ${f.mono};
      font-size: ${x.xs};
    `}};function ie(){const t=B.useContext(G),[s]=B.useState(()=>Ue(t));return s}function se(){const t=j.useId();return e.jsx("svg",{xmlns:"http://www.w3.org/2000/svg",enableBackground:"new 0 0 634 633",viewBox:"0 0 634 633",children:e.jsxs("g",{transform:"translate(1)",children:[e.jsxs("linearGradient",{id:`a-${t}`,x1:"-641.486",x2:"-641.486",y1:"856.648",y2:"855.931",gradientTransform:"matrix(633 0 0 -633 406377 542258)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#6bdaff"}),e.jsx("stop",{offset:"0.319",stopColor:"#f9ffb5"}),e.jsx("stop",{offset:"0.706",stopColor:"#ffa770"}),e.jsx("stop",{offset:"1",stopColor:"#ff7373"})]}),e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:`url(#a-${t})`,fillRule:"evenodd",clipRule:"evenodd"}),e.jsx("defs",{children:e.jsx("filter",{id:`b-${t}`,width:"454",height:"396.9",x:"-137.5",y:"412",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`c-${t}`,width:"454",height:"396.9",x:"-137.5",y:"412",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#b-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"89.5",cy:"610.5",fill:"#015064",fillRule:"evenodd",stroke:"#00CFE2",strokeWidth:"25",clipRule:"evenodd",mask:`url(#c-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`d-${t}`,width:"454",height:"396.9",x:"316.5",y:"412",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`e-${t}`,width:"454",height:"396.9",x:"316.5",y:"412",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#d-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"543.5",cy:"610.5",fill:"#015064",fillRule:"evenodd",stroke:"#00CFE2",strokeWidth:"25",clipRule:"evenodd",mask:`url(#e-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`f-${t}`,width:"454",height:"396.9",x:"-137.5",y:"450",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`g-${t}`,width:"454",height:"396.9",x:"-137.5",y:"450",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#f-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"89.5",cy:"648.5",fill:"#015064",fillRule:"evenodd",stroke:"#00A8B8",strokeWidth:"25",clipRule:"evenodd",mask:`url(#g-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`h-${t}`,width:"454",height:"396.9",x:"316.5",y:"450",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`i-${t}`,width:"454",height:"396.9",x:"316.5",y:"450",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#h-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"543.5",cy:"648.5",fill:"#015064",fillRule:"evenodd",stroke:"#00A8B8",strokeWidth:"25",clipRule:"evenodd",mask:`url(#i-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`j-${t}`,width:"454",height:"396.9",x:"-137.5",y:"486",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`k-${t}`,width:"454",height:"396.9",x:"-137.5",y:"486",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#j-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"89.5",cy:"684.5",fill:"#015064",fillRule:"evenodd",stroke:"#007782",strokeWidth:"25",clipRule:"evenodd",mask:`url(#k-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`l-${t}`,width:"454",height:"396.9",x:"316.5",y:"486",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`m-${t}`,width:"454",height:"396.9",x:"316.5",y:"486",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#l-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("ellipse",{cx:"543.5",cy:"684.5",fill:"#015064",fillRule:"evenodd",stroke:"#007782",strokeWidth:"25",clipRule:"evenodd",mask:`url(#m-${t})`,rx:"214.5",ry:"186"}),e.jsx("defs",{children:e.jsx("filter",{id:`n-${t}`,width:"176.9",height:"129.3",x:"272.2",y:"308",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`o-${t}`,width:"176.9",height:"129.3",x:"272.2",y:"308",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#n-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsxs("g",{mask:`url(#o-${t})`,children:[e.jsx("path",{fill:"none",stroke:"#000",strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"11",d:"M436 403.2l-5 28.6m-140-90.3l-10.9 62m52.8-19.4l-4.3 27.1"}),e.jsxs("linearGradient",{id:`p-${t}`,x1:"-645.656",x2:"-646.499",y1:"854.878",y2:"854.788",gradientTransform:"matrix(-184.159 -32.4722 11.4608 -64.9973 -128419.844 34938.836)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ee2700"}),e.jsx("stop",{offset:"1",stopColor:"#ff008e"})]}),e.jsx("path",{fill:`url(#p-${t})`,fillRule:"evenodd",d:"M344.1 363l97.7 17.2c5.8 2.1 8.2 6.2 7.1 12.1-1 5.9-4.7 9.2-11 9.9l-106-18.7-57.5-59.2c-3.2-4.8-2.9-9.1.8-12.8 3.7-3.7 8.3-4.4 13.7-2.1l55.2 53.6z",clipRule:"evenodd"}),e.jsx("path",{fill:"#D8D8D8",fillRule:"evenodd",stroke:"#FFF",strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"7",d:"M428.3 384.5l.9-6.5m-33.9 1.5l.9-6.5m-34 .5l.9-6.1m-38.9-16.1l4.2-3.9m-25.2-16.1l4.2-3.9",clipRule:"evenodd"})]}),e.jsx("defs",{children:e.jsx("filter",{id:`q-${t}`,width:"280.6",height:"317.4",x:"73.2",y:"113.9",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`r-${t}`,width:"280.6",height:"317.4",x:"73.2",y:"113.9",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#q-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsxs("g",{mask:`url(#r-${t})`,children:[e.jsxs("linearGradient",{id:`s-${t}`,x1:"-646.8",x2:"-646.8",y1:"854.844",y2:"853.844",gradientTransform:"matrix(-100.1751 48.8587 -97.9753 -200.879 19124.773 203538.61)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#a17500"}),e.jsx("stop",{offset:"1",stopColor:"#5d2100"})]}),e.jsx("path",{fill:`url(#s-${t})`,fillRule:"evenodd",d:"M192.3 203c8.1 37.3 14 73.6 17.8 109.1 3.8 35.4 2.8 75.2-2.9 119.2l61.2-16.7c-15.6-59-25.2-97.9-28.6-116.6-3.4-18.7-10.8-51.8-22.2-99.6l-25.3 4.6",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`t-${t}`,x1:"-635.467",x2:"-635.467",y1:"852.115",y2:"851.115",gradientTransform:"matrix(92.6873 4.8575 2.0257 -38.6535 57323.695 36176.047)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#t-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M195 183.9s-12.6-22.1-36.5-29.9c-15.9-5.2-34.4-1.5-55.5 11.1 15.9 14.3 29.5 22.6 40.7 24.9 16.8 3.6 51.3-6.1 51.3-6.1z",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`u-${t}`,x1:"-636.573",x2:"-636.573",y1:"855.444",y2:"854.444",gradientTransform:"matrix(109.9945 5.7646 6.3597 -121.3507 64719.133 107659.336)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#u-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M194.9 184.5s-47.5-8.5-83.2 15.7c-23.8 16.2-34.3 49.3-31.6 99.3 30.3-27.8 52.1-48.5 65.2-61.9 19.8-20 49.6-53.1 49.6-53.1z",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`v-${t}`,x1:"-632.145",x2:"-632.145",y1:"854.174",y2:"853.174",gradientTransform:"matrix(62.9558 3.2994 3.5021 -66.8246 37035.367 59284.227)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#v-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M195 183.9c-.8-21.9 6-38 20.6-48.2 14.6-10.2 29.8-15.3 45.5-15.3-6.1 21.4-14.5 35.8-25.2 43.4-10.7 7.5-24.4 14.2-40.9 20.1z",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`w-${t}`,x1:"-638.224",x2:"-638.224",y1:"853.801",y2:"852.801",gradientTransform:"matrix(152.4666 7.9904 3.0934 -59.0251 94939.86 55646.855)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#w-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M194.9 184.5c31.9-30 64.1-39.7 96.7-29 32.6 10.7 50.8 30.4 54.6 59.1-35.2-5.5-60.4-9.6-75.8-12.1-15.3-2.6-40.5-8.6-75.5-18z",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`x-${t}`,x1:"-637.723",x2:"-637.723",y1:"855.103",y2:"854.103",gradientTransform:"matrix(136.467 7.1519 5.2165 -99.5377 82830.875 89859.578)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#x-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M194.9 184.5c35.8-7.6 65.6-.2 89.2 22 23.6 22.2 37.7 49 42.3 80.3-39.8-9.7-68.3-23.8-85.5-42.4-17.2-18.5-32.5-38.5-46-59.9z",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`y-${t}`,x1:"-631.79",x2:"-631.79",y1:"855.872",y2:"854.872",gradientTransform:"matrix(60.8683 3.19 8.7771 -167.4773 31110.818 145537.61)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#2f8a00"}),e.jsx("stop",{offset:"1",stopColor:"#90ff57"})]}),e.jsx("path",{fill:`url(#y-${t})`,fillRule:"evenodd",stroke:"#2F8A00",strokeWidth:"13",d:"M194.9 184.5c-33.6 13.8-53.6 35.7-60.1 65.6-6.5 29.9-3.6 63.1 8.7 99.6 27.4-40.3 43.2-69.6 47.4-88 4.2-18.3 5.5-44.1 4-77.2z",clipRule:"evenodd"}),e.jsx("path",{fill:"none",stroke:"#2F8A00",strokeLinecap:"round",strokeWidth:"8",d:"M196.5 182.3c-14.8 21.6-25.1 41.4-30.8 59.4-5.7 18-9.4 33-11.1 45.1"}),e.jsx("path",{fill:"none",stroke:"#2F8A00",strokeLinecap:"round",strokeWidth:"8",d:"M194.8 185.7c-24.4 1.7-43.8 9-58.1 21.8-14.3 12.8-24.7 25.4-31.3 37.8m99.1-68.9c29.7-6.7 52-8.4 67-5 15 3.4 26.9 8.7 35.8 15.9m-110.8-5.9c20.3 9.9 38.2 20.5 53.9 31.9 15.7 11.4 27.4 22.1 35.1 32"})]}),e.jsx("defs",{children:e.jsx("filter",{id:`z-${t}`,width:"532",height:"633",x:"50.5",y:"399",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`A-${t}`,width:"532",height:"633",x:"50.5",y:"399",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#z-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsxs("linearGradient",{id:`B-${t}`,x1:"-641.104",x2:"-641.278",y1:"856.577",y2:"856.183",gradientTransform:"matrix(532 0 0 -633 341484.5 542657)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#fff400"}),e.jsx("stop",{offset:"1",stopColor:"#3c8700"})]}),e.jsx("ellipse",{cx:"316.5",cy:"715.5",fill:`url(#B-${t})`,fillRule:"evenodd",clipRule:"evenodd",mask:`url(#A-${t})`,rx:"266",ry:"316.5"}),e.jsx("defs",{children:e.jsx("filter",{id:`C-${t}`,width:"288",height:"283",x:"391",y:"-24",filterUnits:"userSpaceOnUse",children:e.jsx("feColorMatrix",{values:"1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0"})})}),e.jsx("mask",{id:`D-${t}`,width:"288",height:"283",x:"391",y:"-24",maskUnits:"userSpaceOnUse",children:e.jsx("g",{filter:`url(#C-${t})`,children:e.jsx("circle",{cx:"316.5",cy:"316.5",r:"316.5",fill:"#FFF",fillRule:"evenodd",clipRule:"evenodd"})})}),e.jsx("g",{mask:`url(#D-${t})`,children:e.jsxs("g",{transform:"translate(397 -24)",children:[e.jsxs("linearGradient",{id:`E-${t}`,x1:"-1036.672",x2:"-1036.672",y1:"880.018",y2:"879.018",gradientTransform:"matrix(227 0 0 -227 235493 199764)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffdf00"}),e.jsx("stop",{offset:"1",stopColor:"#ff9d00"})]}),e.jsx("circle",{cx:"168.5",cy:"113.5",r:"113.5",fill:`url(#E-${t})`,fillRule:"evenodd",clipRule:"evenodd"}),e.jsxs("linearGradient",{id:`F-${t}`,x1:"-1017.329",x2:"-1018.602",y1:"658.003",y2:"657.998",gradientTransform:"matrix(30 0 0 -1 30558 771)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#F-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M30 113H0"}),e.jsxs("linearGradient",{id:`G-${t}`,x1:"-1014.501",x2:"-1015.774",y1:"839.985",y2:"839.935",gradientTransform:"matrix(26.5 0 0 -5.5 26925 4696.5)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#G-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M33.5 79.5L7 74"}),e.jsxs("linearGradient",{id:`H-${t}`,x1:"-1016.59",x2:"-1017.862",y1:"852.671",y2:"852.595",gradientTransform:"matrix(29 0 0 -8 29523 6971)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#H-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M34 146l-29 8"}),e.jsxs("linearGradient",{id:`I-${t}`,x1:"-1011.984",x2:"-1013.257",y1:"863.523",y2:"863.229",gradientTransform:"matrix(24 0 0 -13 24339 11407)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#I-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M45 177l-24 13"}),e.jsxs("linearGradient",{id:`J-${t}`,x1:"-1006.673",x2:"-1007.946",y1:"869.279",y2:"868.376",gradientTransform:"matrix(20 0 0 -19 20205 16720)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#J-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M67 204l-20 19"}),e.jsxs("linearGradient",{id:`K-${t}`,x1:"-992.85",x2:"-993.317",y1:"871.258",y2:"870.258",gradientTransform:"matrix(13.8339 0 0 -22.8467 13825.796 20131.938)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#K-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M94.4 227l-13.8 22.8"}),e.jsxs("linearGradient",{id:`L-${t}`,x1:"-953.835",x2:"-953.965",y1:"871.9",y2:"870.9",gradientTransform:"matrix(7.5 0 0 -24.5 7278 21605)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#L-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M127.5 243.5L120 268"}),e.jsxs("linearGradient",{id:`M-${t}`,x1:"244.504",x2:"244.496",y1:"871.898",y2:"870.898",gradientTransform:"matrix(.5 0 0 -24.5 45.5 21614)",gradientUnits:"userSpaceOnUse",children:[e.jsx("stop",{offset:"0",stopColor:"#ffa400"}),e.jsx("stop",{offset:"1",stopColor:"#ff5e00"})]}),e.jsx("path",{fill:"none",stroke:`url(#M-${t})`,strokeLinecap:"round",strokeLinejoin:"bevel",strokeWidth:"12",d:"M167.5 252.5l.5 24.5"})]})})]})})}function De(t){const{className:s,...o}=t,r=T();return e.jsxs("button",{...o,className:b(r.logo,s),children:[e.jsx("div",{className:r.tanstackLogo,children:"TANSTACK"}),e.jsx("div",{className:r.routerLogo,children:"React Router v1"})]})}function Le(t){const{shadowDOMTarget:s}=t;return e.jsx(G.Provider,{value:s,children:e.jsx(Me,{...t})})}function Me({initialIsOpen:t,panelProps:s={},closeButtonProps:o={},toggleButtonProps:r={},position:u="bottom-left",containerElement:l="footer",router:c,shadowDOMTarget:f}){const[d,x]=j.useState(),n=j.useRef(null),[a,i]=P("tanstackRouterDevtoolsOpen",t),[g,p]=P("tanstackRouterDevtoolsHeight",null),[k,C]=ee(!1),[m,w]=ee(!1),U=oe(),y=T(),O=(F,R)=>{if(R.button!==0)return;w(!0);const D={originalHeight:(F==null?void 0:F.getBoundingClientRect().height)??0,pageY:R.pageY},L=fe=>{const ue=D.pageY-fe.pageY,Z=D.originalHeight+ue;p(Z),Z<70?i(!1):i(!0)},A=()=>{w(!1),document.removeEventListener("mousemove",L),document.removeEventListener("mouseUp",A)};document.addEventListener("mousemove",L),document.addEventListener("mouseup",A)},$=a??!1;j.useEffect(()=>{C(a??!1)},[a,k,C]),j.useEffect(()=>{var F;if(k){const R=(F=d==null?void 0:d.parentElement)==null?void 0:F.style.paddingBottom,D=()=>{var L;const A=(L=n.current)==null?void 0:L.getBoundingClientRect().height;d!=null&&d.parentElement&&(d.parentElement.style.paddingBottom=`${A}px`)};if(D(),typeof window<"u")return window.addEventListener("resize",D),()=>{window.removeEventListener("resize",D),d!=null&&d.parentElement&&typeof R=="string"&&(d.parentElement.style.paddingBottom=R)}}},[k,d==null?void 0:d.parentElement]),j.useEffect(()=>{if(d){const F=d,R=getComputedStyle(F).fontSize;F.style.setProperty("--tsrd-font-size",R)}},[d]);const{style:H={},...I}=s,{style:h={},onClick:z,...Ee}=o,{onClick:q,className:de,...ce}=r;if(!U)return null;const K=g??500;return e.jsxs(l,{ref:x,className:"TanStackRouterDevtools",children:[e.jsx(J.Provider,{value:{onCloseClick:z??(()=>{})},children:e.jsx(le,{ref:n,...I,router:c,className:b(y.devtoolsPanelContainer,y.devtoolsPanelContainerVisibility(!!a),y.devtoolsPanelContainerResizing(m),y.devtoolsPanelContainerAnimation(k,K+16)),style:{height:K,...H},isOpen:k,setIsOpen:i,handleDragStart:F=>O(n.current,F),shadowDOMTarget:f})}),e.jsxs("button",{type:"button",...ce,"aria-label":"Open TanStack Router Devtools",onClick:F=>{i(!0),q&&q(F)},className:b(y.mainCloseBtn,y.mainCloseBtnPosition(u),y.mainCloseBtnAnimation(!$),de),children:[e.jsxs("div",{className:y.mainCloseBtnIconContainer,children:[e.jsx("div",{className:y.mainCloseBtnIconOuter,children:e.jsx(se,{})}),e.jsx("div",{className:y.mainCloseBtnIconInner,children:e.jsx(se,{})})]}),e.jsx("div",{className:y.mainCloseBtnDivider,children:"-"}),e.jsx("div",{className:y.routerLogoCloseButton,children:"TanStack Router"})]})]})}const Te=j.forwardRef(function(s,o){const{shadowDOMTarget:r}=s;return e.jsx(G.Provider,{value:r,children:e.jsx(J.Provider,{value:{onCloseClick:()=>{}},children:e.jsx(le,{ref:o,...s})})})});function ae({router:t,route:s,isRoot:o,activeId:r,setActiveId:u}){var l;const c=ne({router:t}),f=T(),d=c.pendingMatches||c.matches,x=c.matches.find(a=>a.routeId===s.id),n=j.useMemo(()=>{try{if(x!=null&&x.params){const a=x.params,i=s.path||Q(s.id);if(i.startsWith("$")){const g=i.slice(1);if(a[g])return`(${a[g]})`}}return""}catch{return""}},[x,s]);return e.jsxs("div",{children:[e.jsxs("div",{role:"button","aria-label":`Open match details for ${s.id}`,onClick:()=>{x&&u(r===s.id?"":s.id)},className:b(f.routesRowContainer(s.id===r,!!x)),children:[e.jsx("div",{className:b(f.matchIndicator(ke(d,s)))}),e.jsxs("div",{className:b(f.routesRow(!!x)),children:[e.jsxs("div",{children:[e.jsxs("code",{className:f.code,children:[o?_:s.path||Q(s.id)," "]}),e.jsx("code",{className:f.routeParamInfo,children:n})]}),e.jsx(Y,{match:x,router:t})]})]}),(l=s.children)!=null&&l.length?e.jsx("div",{className:f.nestedRouteRow(!!o),children:[...s.children].sort((a,i)=>a.rank-i.rank).map(a=>e.jsx(ae,{router:t,route:a,activeId:r,setActiveId:u},a.id))}):null]})}const le=j.forwardRef(function(s,o){var r,u;const{isOpen:l=!0,setIsOpen:c,handleDragStart:f,router:d,shadowDOMTarget:x,...n}=s,{onCloseClick:a}=Fe(),i=T(),{className:g,...p}=n,k=xe({warn:!1}),C=d??k,m=ne({router:C});pe(C,"No router was found for the TanStack Router Devtools. Please place the devtools in the <RouterProvider> component tree or pass the router instance to the devtools manually.");const[w,U]=P("tanstackRouterDevtoolsShowMatches",!0),[y,O]=P("tanstackRouterDevtoolsActiveRouteId",""),$=j.useMemo(()=>[...m.pendingMatches??[],...m.matches,...m.cachedMatches].find(z=>z.routeId===y||z.id===y),[y,m.cachedMatches,m.matches,m.pendingMatches]),H=Object.keys(m.location.search).length,I={...C,state:C.state};return e.jsxs("div",{ref:o,className:b(i.devtoolsPanel,"TanStackRouterDevtoolsPanel",g),...p,children:[f?e.jsx("div",{className:i.dragHandle,onMouseDown:f}):null,e.jsx("button",{className:i.panelCloseBtn,onClick:h=>{c(!1),a(h)},children:e.jsx("svg",{xmlns:"http://www.w3.org/2000/svg",width:"10",height:"6",fill:"none",viewBox:"0 0 10 6",className:i.panelCloseBtnIcon,children:e.jsx("path",{stroke:"currentColor",strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"1.667",d:"M1 1l4 4 4-4"})})}),e.jsxs("div",{className:i.firstContainer,children:[e.jsx("div",{className:i.row,children:e.jsx(De,{"aria-hidden":!0,onClick:h=>{c(!1),a(h)}})}),e.jsx("div",{className:i.routerExplorerContainer,children:e.jsx("div",{className:i.routerExplorer,children:e.jsx(M,{label:"Router",value:Object.fromEntries(ze(Object.keys(I),["state","routesById","routesByPath","flatRoutes","options","manifest"].map(h=>z=>z!==h)).map(h=>[h,I[h]]).filter(h=>typeof h[1]!="function"&&!["__store","basepath","injectedHtml","subscribers","latestLoadPromise","navigateTimeout","resetNextScroll","tempLocationKey","latestLocation","routeTree","history"].includes(h[0]))),defaultExpanded:{state:{},context:{},options:{}},filterSubEntries:h=>h.filter(z=>typeof z.value!="function")})})})]}),e.jsxs("div",{className:i.secondContainer,children:[e.jsxs("div",{className:i.matchesContainer,children:[e.jsxs("div",{className:i.detailsHeader,children:[e.jsx("span",{children:"Pathname"}),m.location.maskedLocation?e.jsx("div",{className:i.maskedBadgeContainer,children:e.jsx("span",{className:i.maskedBadge,children:"masked"})}):null]}),e.jsxs("div",{className:i.detailsContent,children:[e.jsx("code",{children:m.location.pathname}),m.location.maskedLocation?e.jsx("code",{className:i.maskedLocation,children:m.location.maskedLocation.pathname}):null]}),e.jsxs("div",{className:i.detailsHeader,children:[e.jsxs("div",{className:i.routeMatchesToggle,children:[e.jsx("button",{type:"button",onClick:()=>{U(!1)},disabled:!w,className:b(i.routeMatchesToggleBtn(!w,!0)),children:"Routes"}),e.jsx("button",{type:"button",onClick:()=>{U(!0)},disabled:w,className:b(i.routeMatchesToggleBtn(!!w,!1)),children:"Matches"})]}),e.jsx("div",{className:i.detailsHeaderInfo,children:e.jsx("div",{children:"age / staleTime / gcTime"})})]}),e.jsx("div",{className:b(i.routesContainer),children:w?e.jsx("div",{children:((r=m.pendingMatches)!=null&&r.length?m.pendingMatches:m.matches).map((h,z)=>e.jsxs("div",{role:"button","aria-label":`Open match details for ${h.id}`,onClick:()=>O(y===h.id?"":h.id),className:b(i.matchRow(h===$)),children:[e.jsx("div",{className:b(i.matchIndicator(V(h)))}),e.jsx("code",{className:i.matchID,children:`${h.routeId===_?_:h.pathname}`}),e.jsx(Y,{match:h,router:C})]},h.id||z))}):e.jsx(ae,{router:C,route:C.routeTree,isRoot:!0,activeId:y,setActiveId:O})})]}),m.cachedMatches.length?e.jsxs("div",{className:i.cachedMatchesContainer,children:[e.jsxs("div",{className:i.detailsHeader,children:[e.jsx("div",{children:"Cached Matches"}),e.jsx("div",{className:i.detailsHeaderInfo,children:"age / staleTime / gcTime"})]}),e.jsx("div",{children:m.cachedMatches.map(h=>e.jsxs("div",{role:"button","aria-label":`Open match details for ${h.id}`,onClick:()=>O(y===h.id?"":h.id),className:b(i.matchRow(h===$)),children:[e.jsx("div",{className:b(i.matchIndicator(V(h)))}),e.jsx("code",{className:i.matchID,children:`${h.id}`}),e.jsx(Y,{match:h,router:C})]},h.id))})]}):null]}),$?e.jsxs("div",{className:i.thirdContainer,children:[e.jsx("div",{className:i.detailsHeader,children:"Match Details"}),e.jsx("div",{children:e.jsxs("div",{className:i.matchDetails,children:[e.jsx("div",{className:i.matchStatus($.status,$.isFetching),children:e.jsx("div",{children:$.status==="success"&&$.isFetching?"fetching":$.status})}),e.jsxs("div",{className:i.matchDetailsInfoLabel,children:[e.jsx("div",{children:"ID:"}),e.jsx("div",{className:i.matchDetailsInfo,children:e.jsx("code",{children:$.id})})]}),e.jsxs("div",{className:i.matchDetailsInfoLabel,children:[e.jsx("div",{children:"State:"}),e.jsx("div",{className:i.matchDetailsInfo,children:(u=m.pendingMatches)!=null&&u.find(h=>h.id===$.id)?"Pending":m.matches.find(h=>h.id===$.id)?"Active":"Cached"})]}),e.jsxs("div",{className:i.matchDetailsInfoLabel,children:[e.jsx("div",{children:"Last Updated:"}),e.jsx("div",{className:i.matchDetailsInfo,children:$.updatedAt?new Date($.updatedAt).toLocaleTimeString():"N/A"})]})]})}),$.loaderData?e.jsxs(e.Fragment,{children:[e.jsx("div",{className:i.detailsHeader,children:"Loader Data"}),e.jsx("div",{className:i.detailsContent,children:e.jsx(M,{label:"loaderData",value:$.loaderData,defaultExpanded:{}})})]}):null,e.jsx("div",{className:i.detailsHeader,children:"Explorer"}),e.jsx("div",{className:i.detailsContent,children:e.jsx(M,{label:"Match",value:$,defaultExpanded:{}})})]}):null,H?e.jsxs("div",{className:i.fourthContainer,children:[e.jsx("div",{className:i.detailsHeader,children:"Search Params"}),e.jsx("div",{className:i.detailsContent,children:e.jsx(M,{value:m.location.search,defaultExpanded:Object.keys(m.location.search).reduce((h,z)=>(h[z]={},h),{})})})]}):null]})});function Y({match:t,router:s}){const o=T(),r=j.useReducer(()=>({}),()=>({}))[1];if(j.useEffect(()=>{const d=setInterval(()=>{r()},1e3);return()=>{clearInterval(d)}},[r]),!t)return null;const u=s.looseRoutesById[t.routeId];if(!u.options.loader)return null;const l=Date.now()-t.updatedAt,c=u.options.staleTime??s.options.defaultStaleTime??0,f=u.options.gcTime??s.options.defaultGcTime??30*60*1e3;return e.jsxs("div",{className:b(o.ageTicker(l>c)),children:[e.jsx("div",{children:W(l)}),e.jsx("div",{children:"/"}),e.jsx("div",{children:W(c)}),e.jsx("div",{children:"/"}),e.jsx("div",{children:W(f)})]})}function W(t){const s=["s","min","h","d"],o=[t/1e3,t/6e4,t/36e5,t/864e5];let r=0;for(let l=1;l<o.length&&!(o[l]<1);l++)r=l;return new Intl.NumberFormat(navigator.language,{compactDisplay:"short",notation:"compact",maximumFractionDigits:0}).format(o[r])+s[r]}const Be=t=>{const{colors:s,font:o,size:r,alpha:u,shadow:l,border:c}=v,{fontFamily:f,lineHeight:d,size:x}=o,n=t?E.bind({target:t}):E;return{devtoolsPanelContainer:n`
      direction: ltr;
      position: fixed;
      bottom: 0;
      right: 0;
      z-index: 99999;
      width: 100%;
      max-height: 90%;
      border-top: 1px solid ${s.gray[700]};
      transform-origin: top;
    `,devtoolsPanelContainerVisibility:a=>n`
        visibility: ${a?"visible":"hidden"};
      `,devtoolsPanelContainerResizing:a=>a?n`
          transition: none;
        `:n`
        transition: all 0.4s ease;
      `,devtoolsPanelContainerAnimation:(a,i)=>a?n`
          pointer-events: auto;
          transform: translateY(0);
        `:n`
        pointer-events: none;
        transform: translateY(${i}px);
      `,logo:n`
      cursor: pointer;
      display: flex;
      flex-direction: column;
      background-color: transparent;
      border: none;
      font-family: ${f.sans};
      gap: ${v.size[.5]};
      padding: 0px;
      &:hover {
        opacity: 0.7;
      }
      &:focus-visible {
        outline-offset: 4px;
        border-radius: ${c.radius.xs};
        outline: 2px solid ${s.blue[800]};
      }
    `,tanstackLogo:n`
      font-size: ${o.size.md};
      font-weight: ${o.weight.bold};
      line-height: ${o.lineHeight.xs};
      white-space: nowrap;
      color: ${s.gray[300]};
    `,routerLogo:n`
      font-weight: ${o.weight.semibold};
      font-size: ${o.size.xs};
      background: linear-gradient(to right, #84cc16, #10b981);
      background-clip: text;
      -webkit-background-clip: text;
      line-height: 1;
      -webkit-text-fill-color: transparent;
      white-space: nowrap;
    `,devtoolsPanel:n`
      display: flex;
      font-size: ${x.sm};
      font-family: ${f.sans};
      background-color: ${s.darkGray[700]};
      color: ${s.gray[300]};

      @media (max-width: 700px) {
        flex-direction: column;
      }
      @media (max-width: 600px) {
        font-size: ${x.xs};
      }
    `,dragHandle:n`
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 4px;
      cursor: row-resize;
      z-index: 100000;
      &:hover {
        background-color: ${s.purple[400]}${u[90]};
      }
    `,firstContainer:n`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      border-right: 1px solid ${s.gray[700]};
      display: flex;
      flex-direction: column;
    `,routerExplorerContainer:n`
      overflow-y: auto;
      flex: 1;
    `,routerExplorer:n`
      padding: ${v.size[2]};
    `,row:n`
      display: flex;
      align-items: center;
      padding: ${v.size[2]} ${v.size[2.5]};
      gap: ${v.size[2.5]};
      border-bottom: ${s.darkGray[500]} 1px solid;
      align-items: center;
    `,detailsHeader:n`
      font-family: ui-sans-serif, Inter, system-ui, sans-serif, sans-serif;
      position: sticky;
      top: 0;
      z-index: 2;
      background-color: ${s.darkGray[600]};
      padding: 0px ${v.size[2]};
      font-weight: ${o.weight.medium};
      font-size: ${o.size.xs};
      min-height: ${v.size[8]};
      line-height: ${o.lineHeight.xs};
      text-align: left;
      display: flex;
      align-items: center;
    `,maskedBadge:n`
      background: ${s.yellow[900]}${u[70]};
      color: ${s.yellow[300]};
      display: inline-block;
      padding: ${v.size[0]} ${v.size[2.5]};
      border-radius: ${c.radius.full};
      font-size: ${o.size.xs};
      font-weight: ${o.weight.normal};
      border: 1px solid ${s.yellow[300]};
    `,maskedLocation:n`
      color: ${s.yellow[300]};
    `,detailsContent:n`
      padding: ${v.size[1.5]} ${v.size[2]};
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: ${o.size.xs};
    `,routeMatchesToggle:n`
      display: flex;
      align-items: center;
      border: 1px solid ${s.gray[500]};
      border-radius: ${c.radius.sm};
      overflow: hidden;
    `,routeMatchesToggleBtn:(a,i)=>{const p=[n`
        appearance: none;
        border: none;
        font-size: 12px;
        padding: 4px 8px;
        background: transparent;
        cursor: pointer;
        font-family: ${f.sans};
        font-weight: ${o.weight.medium};
      `];if(a){const k=n`
          background: ${s.darkGray[400]};
          color: ${s.gray[300]};
        `;p.push(k)}else{const k=n`
          color: ${s.gray[500]};
          background: ${s.darkGray[800]}${u[20]};
        `;p.push(k)}return i&&p.push(n`
          border-right: 1px solid ${v.colors.gray[500]};
        `),p},detailsHeaderInfo:n`
      flex: 1;
      justify-content: flex-end;
      display: flex;
      align-items: center;
      font-weight: ${o.weight.normal};
      color: ${s.gray[400]};
    `,matchRow:a=>{const g=[n`
        display: flex;
        border-bottom: 1px solid ${s.darkGray[400]};
        cursor: pointer;
        align-items: center;
        padding: ${r[1]} ${r[2]};
        gap: ${r[2]};
        font-size: ${x.xs};
        color: ${s.gray[300]};
      `];if(a){const p=n`
          background: ${s.darkGray[500]};
        `;g.push(p)}return g},matchIndicator:a=>{const g=[n`
        flex: 0 0 auto;
        width: ${r[3]};
        height: ${r[3]};
        background: ${s[a][900]};
        border: 1px solid ${s[a][500]};
        border-radius: ${c.radius.full};
        transition: all 0.25s ease-out;
        box-sizing: border-box;
      `];if(a==="gray"){const p=n`
          background: ${s.gray[700]};
          border-color: ${s.gray[400]};
        `;g.push(p)}return g},matchID:n`
      flex: 1;
      line-height: ${d.xs};
    `,ageTicker:a=>{const g=[n`
        display: flex;
        gap: ${r[1]};
        font-size: ${x.xs};
        color: ${s.gray[400]};
        font-variant-numeric: tabular-nums;
        line-height: ${d.xs};
      `];if(a){const p=n`
          color: ${s.yellow[400]};
        `;g.push(p)}return g},secondContainer:n`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      border-right: 1px solid ${s.gray[700]};
      display: flex;
      flex-direction: column;
    `,thirdContainer:n`
      flex: 1 1 500px;
      overflow: auto;
      display: flex;
      flex-direction: column;
      height: 100%;
      border-right: 1px solid ${s.gray[700]};

      @media (max-width: 700px) {
        border-top: 2px solid ${s.gray[700]};
      }
    `,fourthContainer:n`
      flex: 1 1 500px;
      min-height: 40%;
      max-height: 100%;
      overflow: auto;
      display: flex;
      flex-direction: column;
    `,routesContainer:n`
      overflow-x: auto;
      overflow-y: visible;
    `,routesRowContainer:(a,i)=>{const p=[n`
        display: flex;
        border-bottom: 1px solid ${s.darkGray[400]};
        align-items: center;
        padding: ${r[1]} ${r[2]};
        gap: ${r[2]};
        font-size: ${x.xs};
        color: ${s.gray[300]};
        cursor: ${i?"pointer":"default"};
        line-height: ${d.xs};
      `];if(a){const k=n`
          background: ${s.darkGray[500]};
        `;p.push(k)}return p},routesRow:a=>{const g=[n`
        flex: 1 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: ${x.xs};
        line-height: ${d.xs};
      `];if(!a){const p=n`
          color: ${s.gray[400]};
        `;g.push(p)}return g},routeParamInfo:n`
      color: ${s.gray[400]};
      font-size: ${x.xs};
      line-height: ${d.xs};
    `,nestedRouteRow:a=>n`
        margin-left: ${a?0:r[3.5]};
        border-left: ${a?"":`solid 1px ${s.gray[700]}`};
      `,code:n`
      font-size: ${x.xs};
      line-height: ${d.xs};
    `,matchesContainer:n`
      flex: 1 1 auto;
      overflow-y: auto;
    `,cachedMatchesContainer:n`
      flex: 1 1 auto;
      overflow-y: auto;
      max-height: 50%;
    `,maskedBadgeContainer:n`
      flex: 1;
      justify-content: flex-end;
      display: flex;
    `,matchDetails:n`
      display: flex;
      flex-direction: column;
      padding: ${v.size[2]};
      font-size: ${v.font.size.xs};
      color: ${v.colors.gray[300]};
      line-height: ${v.font.lineHeight.sm};
    `,matchStatus:(a,i)=>{const p=i&&a==="success"?i==="beforeLoad"?"purple":"blue":{pending:"yellow",success:"green",error:"red",notFound:"purple",redirected:"gray"}[a];return n`
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40px;
        border-radius: ${v.border.radius.sm};
        font-weight: ${v.font.weight.normal};
        background-color: ${v.colors[p][900]}${v.alpha[90]};
        color: ${v.colors[p][300]};
        border: 1px solid ${v.colors[p][600]};
        margin-bottom: ${v.size[2]};
        transition: all 0.25s ease-out;
      `},matchDetailsInfo:n`
      display: flex;
      justify-content: flex-end;
      flex: 1;
    `,matchDetailsInfoLabel:n`
      display: flex;
    `,mainCloseBtn:n`
      background: ${s.darkGray[700]};
      padding: ${r[1]} ${r[2]} ${r[1]} ${r[1.5]};
      border-radius: ${c.radius.md};
      position: fixed;
      z-index: 99999;
      display: inline-flex;
      width: fit-content;
      cursor: pointer;
      appearance: none;
      border: 0;
      gap: 8px;
      align-items: center;
      border: 1px solid ${s.gray[500]};
      font-size: ${o.size.xs};
      cursor: pointer;
      transition: all 0.25s ease-out;

      &:hover {
        background: ${s.darkGray[500]};
      }
    `,mainCloseBtnPosition:a=>n`
        ${a==="top-left"?`top: ${r[2]}; left: ${r[2]};`:""}
        ${a==="top-right"?`top: ${r[2]}; right: ${r[2]};`:""}
        ${a==="bottom-left"?`bottom: ${r[2]}; left: ${r[2]};`:""}
        ${a==="bottom-right"?`bottom: ${r[2]}; right: ${r[2]};`:""}
      `,mainCloseBtnAnimation:a=>a?n`
          opacity: 1;
          pointer-events: auto;
          visibility: visible;
        `:n`
        opacity: 0;
        pointer-events: none;
        visibility: hidden;
      `,routerLogoCloseButton:n`
      font-weight: ${o.weight.semibold};
      font-size: ${o.size.xs};
      background: linear-gradient(to right, #98f30c, #00f4a3);
      background-clip: text;
      -webkit-background-clip: text;
      line-height: 1;
      -webkit-text-fill-color: transparent;
      white-space: nowrap;
    `,mainCloseBtnDivider:n`
      width: 1px;
      background: ${v.colors.gray[600]};
      height: 100%;
      border-radius: 999999px;
      color: transparent;
    `,mainCloseBtnIconContainer:n`
      position: relative;
      width: ${r[5]};
      height: ${r[5]};
      background: pink;
      border-radius: 999999px;
      overflow: hidden;
    `,mainCloseBtnIconOuter:n`
      width: ${r[5]};
      height: ${r[5]};
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      filter: blur(3px) saturate(1.8) contrast(2);
    `,mainCloseBtnIconInner:n`
      width: ${r[4]};
      height: ${r[4]};
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    `,panelCloseBtn:n`
      position: absolute;
      cursor: pointer;
      z-index: 100001;
      display: flex;
      align-items: center;
      justify-content: center;
      outline: none;
      background-color: ${s.darkGray[700]};
      &:hover {
        background-color: ${s.darkGray[500]};
      }

      top: 0;
      right: ${r[2]};
      transform: translate(0, -100%);
      border-right: ${s.darkGray[300]} 1px solid;
      border-left: ${s.darkGray[300]} 1px solid;
      border-top: ${s.darkGray[300]} 1px solid;
      border-bottom: none;
      border-radius: ${c.radius.sm} ${c.radius.sm} 0px 0px;
      padding: ${r[1]} ${r[1.5]} ${r[.5]} ${r[1.5]};

      &::after {
        content: ' ';
        position: absolute;
        top: 100%;
        left: -${r[2.5]};
        height: ${r[1.5]};
        width: calc(100% + ${r[5]});
      }
    `,panelCloseBtnIcon:n`
      color: ${s.gray[400]};
      width: ${r[2]};
      height: ${r[2]};
    `}};function T(){const t=j.useContext(G),[s]=j.useState(()=>Be(t));return s}export{Le as TanStackRouterDevtools,Te as TanStackRouterDevtoolsPanel};
