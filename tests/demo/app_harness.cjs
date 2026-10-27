/* DOM/renderer boundary doubles for the real synthetic app composition. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const state = require('../../apps/synthetic_demo/web/state.js');
const paths = require('../../apps/synthetic_demo/web/path.js');

function mount(view, {renderer=true,draw=true}={}) {
  const nodes = new Map(), listeners = new Map();
  let document, network;
  class Element {
    constructor(tag='div') {
      this.tag=tag;this.dataset={};this.style={};this.children=[];this.attributes={};
      this.listeners=new Map();this.disabled=false;this.value='';this.textContent='';
      this.maxScroll=1000;this.left=0;this.top=0;this.rebuilds=0;
    }
    set scrollTop(value) { this.top=Math.max(0,Math.min(this.maxScroll,value)); }
    get scrollTop() { return this.top; }
    set scrollLeft(value) { this.left=Math.max(0,Math.min(this.maxScroll,value)); }
    get scrollLeft() { return this.left; }
    append(...children) { this.children.push(...children); }
    replaceChildren(...children) { this.children=children;this.scrollTop=0;this.scrollLeft=0;this.rebuilds++; }
    setAttribute(key,value) { this.attributes[key]=value; }
    addEventListener(type,fn) { this.listeners.set(type,fn); }
    emit(type) { this.listeners.get(type)?.({target:this}); }
    focus() { document.activeElement=this; }
    querySelectorAll(tag) {
      return this.children.flatMap(child=>typeof child==='object'
        ? [...(child.tag===tag?[child]:[]),...child.querySelectorAll(tag)] : []);
    }
  }
  const html=fs.readFileSync(path.join(__dirname,'../../apps/synthetic_demo/web/index.html'),'utf8');
  for(const [,id] of html.matchAll(/\bid="([^"]+)"/g)) {
    const element=new Element();element.id=id;nodes.set(id,element);
  }
  const contexts=['all','work','personal'].map(context=>Object.assign(new Element('button'),{dataset:{context}}));
  const categories=['note','project','journal','tag'].map(category=>Object.assign(new Element('input'),{dataset:{category}}));
  const page=new Element();
  document={activeElement:null,scrollingElement:page,createElement:tag=>new Element(tag),
    getElementById:id=>nodes.get(id),
    querySelectorAll:selector=>selector==='[data-context]'?contexts:categories,
    addEventListener:(type,fn)=>listeners.set(type,fn)};
  nodes.get('demo-data').textContent=JSON.stringify(view);
  class Network {
    constructor() {network=this;this.camera={x:0,y:0,scale:1};this.events=new Map();this.onceEvents=new Map();this.moves=[];this.focuses=[];this.pending=null;}
    on(type,fn) {this.events.set(type,fn);}
    once(type,fn) {this.onceEvents.set(type,fn);}
    emit(type,event={}) {this.events.get(type)?.(event);const fn=this.onceEvents.get(type);this.onceEvents.delete(type);fn?.(event);}
    getScale() {return this.camera.scale;}
    getViewPosition() {return {x:this.camera.x,y:this.camera.y};}
    // The bundled renderer leaves a pre-first-frame transition pending.
    moveTo(options) {this.moves.push(options);Object.assign(this.camera,options.position, {scale:options.scale??this.camera.scale});}
    fit() {this.moveTo({position:{x:0,y:0},scale:1,animation:false});}
    focus(id,options) {
      this.focuses.push(options);
      const n=view.nodes.find(n=>n.id===id), target={x:n.x??50,y:n.y??60,scale:options.scale};
      if(options.animation) {this.pending=target;this.camera={...target,x:target.x/2};}
      else this.camera=target;
    }
    finishAnimation() {if(this.pending)this.camera=this.pending;this.pending=null;this.emit('animationFinished');}
    selectNodes() {}
    unselectAll() {}
  }
  class DataSet {constructor(){} update(){} }
  const window={TramaDemoState:state,TramaDemoPath:paths,matchMedia:()=>({matches:false})};
  if(renderer)window.vis={Network,DataSet};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../../apps/synthetic_demo/web/app.js'),'utf8'),{window,document});
  if(draw)network?.emit('afterDrawing');
  const click=id=>{const node=nodes.get(id);node.focus();if(!node.disabled)node.emit('click');};
  const select=id=>{const button=nodes.get('node-list').querySelectorAll('button').find(b=>b.dataset.nodeId===id);button.focus();button.emit('click');};
  const search=value=>{const input=nodes.get('search');input.value=value;input.focus();input.emit('input');};
  const setPresentation=value=>{
    if(network&&value.camera)network.camera={...value.camera};
    for(const [key,node]of[['page',page],['list',nodes.get('node-list')],['details',nodes.get('details')]]) {
      node.scrollLeft=value.scroll[key].x;node.scrollTop=value.scroll[key].y;
    }
  };
  const presentation=()=>({camera:network?{...network.camera}:null,scroll:Object.fromEntries(
    [['page',page],['list',nodes.get('node-list')],['details',nodes.get('details')]]
      .map(([key,node])=>[key,{x:node.scrollLeft,y:node.scrollTop}]))});
  return {nodes,network,document,page,contexts,click,select,search,setPresentation,presentation,
    scroll:()=>listeners.get('scroll')?.()};
}
module.exports={mount};
