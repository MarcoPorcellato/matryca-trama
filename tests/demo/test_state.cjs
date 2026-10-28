const test = require('node:test');
const assert = require('node:assert/strict');
const { initialState, reduceState, visibleGraph, neighbors, suggestedNode, filteredGraph, initialHistory, historyState, reduceHistory } = require('../../apps/synthetic_demo/web/state.js');
const { historyPresentation, rememberPresentation } = require('../../apps/synthetic_demo/web/state.js');
const view = { nodes: [
  {id:'a',label:'Café and ideas',category:'note',spaces:['personal']},
  {id:'b',label:'Project Lighthouse',category:'project',spaces:['work']},
  {id:'c',label:'Ada',category:'note',spaces:['personal','work']},
  {id:'d',label:'Daily journal',category:'journal',spaces:['personal']},
], edges:[{id:'ab',from:'a',to:'b'},{id:'bc',from:'b',to:'c'},{id:'cd',from:'c',to:'d'}] };
test('search is case and accent insensitive', () => {
  const state = reduceState(view, initialState(), {type:'search',value:'CAFE'});
  assert.deepEqual(visibleGraph(view,state).nodes.map(n=>n.id), ['a']);
  assert.equal(visibleGraph(view,state).edges.length,0);
});
test('contexts and categories intersect without dangling edges', () => {
  let state = reduceState(view,initialState(),{type:'context',value:'personal'});
  state = reduceState(view,state,{type:'category',value:'journal'});
  assert.deepEqual(visibleGraph(view,state).nodes.map(n=>n.id), ['a','c']);
  assert.deepEqual(visibleGraph(view,state).edges, []);
});
test('hidden selection clears and only visible neighbors are actionable', () => {
  let state = reduceState(view,initialState(),{type:'select',value:'b'});
  assert.equal(state.selected,'b');
  state = reduceState(view,state,{type:'context',value:'personal'});
  assert.equal(state.selected,null);
  assert.deepEqual(neighbors(visibleGraph(view,state),'c'), ['d']);
  state = reduceState(view,state,{type:'select',value:'b'});
  assert.equal(state.selected,null);
});
test('reset restores query, filters and selection after empty results', () => {
  let state = reduceState(view,initialState(),{type:'search',value:'missing'});
  assert.equal(visibleGraph(view,state).nodes.length,0);
  assert.deepEqual(reduceState(view,state,{type:'reset'}),initialState());
  assert.equal(visibleGraph(view,initialState()).edges.length,3);
});
test('the suggested starting node is always visible, including personal and empty views', () => {
  assert.equal(suggestedNode(view,initialState()).id,'b');
  let state=reduceState(view,initialState(),{type:'context',value:'personal'});
  assert.equal(suggestedNode(view,state).id,'a');
  state=reduceState(view,state,{type:'search',value:'missing'});
  assert.equal(suggestedNode(view,state),null);
});

const fullView = {query:'',context:'all',categories:['note','project','journal','tag'],selected:null,scope:'all',pathStart:null,pathEnd:null};
const action = (history,type,value) => reduceHistory(view,history,{type,value});

test('history starts at a stable boundary and supports no movement beyond it', () => {
  assert.equal(typeof initialHistory,'function');
  const history=initialHistory();
  assert.deepEqual(historyState(history),fullView);
  assert.equal(action(history,'back'),history);
  assert.equal(action(history,'forward'),history);
});

test('Back and Forward restore selection together with context and category filters', () => {
  let history=action(initialHistory(),'select','b');
  history=action(history,'context','personal');
  history=action(history,'select','c');
  history=action(history,'category','note');
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null,scope:'all',pathStart:null,pathEnd:null});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'c'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'b'});
  history=action(action(action(history,'forward'),'forward'),'forward');
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null,scope:'all',pathStart:null,pathEnd:null});
});

test('an empty search and its cleared selection are restored as one view', () => {
  let history=action(initialHistory(),'select','c');
  history=action(history,'search','missing');
  assert.equal(visibleGraph(view,historyState(history)).nodes.length,0);
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  history=action(history,'forward');
  assert.deepEqual(historyState(history),{...fullView,query:'missing'});
});

test('consecutive search input is one step and restores the final query verbatim', () => {
  let history=initialHistory();
  for(const query of ['C','Ca','Caf','CAFE'])history=action(history,'search',query);
  assert.equal(history.entries.length,2);
  history=action(history,'back');
  assert.deepEqual(historyState(history),fullView);
  history=action(history,'forward');
  assert.deepEqual(historyState(history),{...fullView,query:'CAFE'});
  assert.deepEqual(visibleGraph(view,historyState(history)).nodes.map(n=>n.id),['a']);
});

test('returning search to its preceding view collapses the step and ends its group', () => {
  let history=action(initialHistory(),'select','c');
  history=action(history,'search','a');
  history=action(history,'search','');
  assert.equal(history.entries.length,2);
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  history=action(history,'search','Ad');
  assert.equal(history.entries.length,3);
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
});

test('category order does not create duplicate views during search collapse', () => {
  const selected={...fullView,categories:['tag','journal','project','note'],selected:'c'};
  const searched={...fullView,query:'a',selected:'c'};
  const history={entries:[selected,searched],index:1,lastAction:'search'};
  const collapsed=action(history,'search','');
  assert.equal(collapsed.entries.length,1);
  assert.deepEqual(historyState(collapsed),selected);
  const next=action(collapsed,'search','Ad');
  assert.equal(next.entries.length,2);
  assert.deepEqual(next.entries[0],selected);
});

test('changed search after Back forks without overwriting the restored predecessor', () => {
  let history=action(initialHistory(),'select','a');
  history=action(history,'select','c');
  history=action(history,'select','b');
  history=action(history,'back');
  const predecessor={...fullView,selected:'c'};
  assert.deepEqual(historyState(history),predecessor);
  history=action(history,'search','Ad');
  history=action(history,'search','Ada');
  assert.deepEqual(history.entries[2],predecessor);
  assert.equal(history.entries.length,4);
  assert.deepEqual(historyState(history),{...fullView,query:'Ada',selected:'c'});
  assert.equal(action(history,'forward'),history);
  assert.deepEqual(historyState(action(history,'back')),predecessor);
});

test('unknown and hidden selections preserve valid selection and the forward path', () => {
  let history=action(initialHistory(),'select','c');
  history=action(history,'context','personal');
  history=action(history,'select','a');
  history=action(history,'back');
  for(const [type,value] of [['select','b'],['select','unknown'],['select','c'],['context','personal'],['context','unknown'],['category','unknown'],['search',''],['unknown',null]]){
    assert.equal(action(history,type,value),history);
  }
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'c'});
  assert.deepEqual(historyState(action(history,'forward')),{...fullView,context:'personal',selected:'a'});
});

test('reset clears the full history including its forward path', () => {
  let history=action(initialHistory(),'context','personal');
  history=action(history,'select','c');
  history=action(history,'search','missing');
  history=action(history,'back');
  history=action(history,'reset');
  assert.deepEqual(historyState(history),fullView);
  assert.equal(history.entries.length,1);
  assert.equal(action(history,'back'),history);
  assert.equal(action(history,'forward'),history);
});

test('history eviction preserves a valid cursor through coalescing and branching', () => {
  let history=initialHistory();
  for(let i=0;i<110;i++)history=action(history,'select',i%2?'c':'a');
  assert.equal(history.entries.length,100);
  assert.equal(history.index,99);
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  for(const query of ['A','Ad','Ada'])history=action(history,'search',query);
  assert.equal(history.entries.length,100);
  assert.equal(history.index,99);
  assert.deepEqual(historyState(history),{...fullView,query:'Ada',selected:'c'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  history=action(history,'context','personal');
  assert.equal(history.entries.length,100);
  assert.equal(history.index,99);
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'c'});
  assert.equal(action(history,'forward'),history);
  for(let i=0;i<110;i++)history=action(history,'back');
  assert.equal(history.index,0);
  assert.equal(action(history,'back'),history);
});

test('history operations leave frozen input snapshots and category arrays untouched', () => {
  let history=action(initialHistory(),'select','c');
  history=action(history,'search','a');
  const before=JSON.stringify(history);
  for(const entry of history.entries){Object.freeze(entry.categories);Object.freeze(entry);}
  Object.freeze(history.entries);Object.freeze(history);
  const changed=action(history,'search','Ad');
  assert.deepEqual(historyState(changed),{...fullView,query:'Ad',selected:'c'});
  assert.equal(JSON.stringify(history),before);
  assert.deepEqual(historyState(action(history,'back')),{...fullView,selected:'c'});
});

const focusView = {nodes:[...view.nodes,{id:'e',label:'#discovery',category:'tag',spaces:['personal','work']}],
  edges:[...view.edges,{id:'ac',from:'a',to:'c'},{id:'de',from:'d',to:'e'}]};
const focusAction = (history,type,value) => reduceHistory(focusView,history,{type,value});
const focusIds = history => visibleGraph(focusView,historyState(history)).nodes.map(n=>n.id);

test('focused view retains the center, immediate neighbors and links among them', () => {
  let history=focusAction(initialHistory(),'select','b');
  history=focusAction(history,'scope','connections');
  assert.equal(historyState(history).scope,'connections');
  assert.deepEqual(focusIds(history),['a','b','c']);
  assert.deepEqual(visibleGraph(focusView,historyState(history)).edges.map(e=>e.id),['ab','bc','ac']);
  assert.deepEqual(filteredGraph(focusView,historyState(history)).nodes.map(n=>n.id),['a','b','c','d','e']);
});

test('focused neighbor travel derives a new neighborhood beyond the preceding view', () => {
  let history=focusAction(initialHistory(),'select','b');
  history=focusAction(history,'scope','connections');
  assert.equal(focusAction(history,'select','d'),history);
  history=focusAction(history,'select','c');
  assert.deepEqual(focusIds(history),['a','b','c','d']);
  assert.deepEqual(visibleGraph(focusView,historyState(history)).edges.map(e=>e.id),['ab','bc','cd','ac']);
  assert.equal(historyState(history).scope,'connections');
});

test('all filter kinds intersect focus and restoring a filter expands its neighborhood', () => {
  let history=focusAction(initialHistory(),'select','c');
  history=focusAction(history,'scope','connections');
  history=focusAction(history,'context','personal');
  assert.deepEqual(focusIds(history),['a','c','d']);
  history=focusAction(history,'category','journal');
  assert.deepEqual(focusIds(history),['a','c']);
  history=focusAction(history,'category','journal');
  assert.deepEqual(focusIds(history),['a','c','d']);
  history=focusAction(history,'search','a');
  assert.deepEqual(focusIds(history),['a','c','d']);
  history=focusAction(history,'search','Ada');
  assert.deepEqual(focusIds(history),['c']);
  assert.equal(visibleGraph(focusView,historyState(history)).edges.length,0);
  assert.equal(historyState(history).scope,'connections');
});

test('hiding the center clears selection and scope together without revealing excluded nodes', () => {
  for(const [type,value,expected] of [['context','personal',['a','c','d','e']],['category','project',['a','c','d','e']],['search','missing',[]]]) {
    let history=focusAction(initialHistory(),'select','b');
    history=focusAction(history,'scope','connections');
    history=focusAction(history,type,value);
    assert.equal(historyState(history).selected,null);
    assert.equal(historyState(history).scope,'all');
    assert.deepEqual(focusIds(history),expected);
    history=focusAction(history,'back');
    assert.equal(historyState(history).selected,'b');
    assert.equal(historyState(history).scope,'connections');
    assert.deepEqual(focusIds(history),['a','b','c']);
  }
});

test('isolated centers remain a one-node view and Show all preserves filters and selection', () => {
  const isolated={nodes:[{id:'alone',label:'An idea',category:'note',spaces:['personal']},
    {id:'other',label:'Another idea',category:'note',spaces:['personal']}],edges:[]};
  let history=reduceHistory(isolated,initialHistory(),{type:'context',value:'personal'});
  history=reduceHistory(isolated,history,{type:'select',value:'alone'});
  history=reduceHistory(isolated,history,{type:'scope',value:'connections'});
  assert.deepEqual(visibleGraph(isolated,historyState(history)),{nodes:[isolated.nodes[0]],edges:[]});
  history=reduceHistory(isolated,history,{type:'scope',value:'all'});
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'alone'});
  assert.deepEqual(visibleGraph(isolated,historyState(history)).nodes.map(n=>n.id),['alone','other']);
});

test('invalid and repeated scope actions preserve Forward and a coalescing search group', () => {
  const start=initialHistory();
  assert.equal(focusAction(start,'scope','connections'),start);
  let history=focusAction(start,'select','c');
  history=focusAction(history,'scope','connections');
  history=focusAction(history,'search','A');
  const length=history.entries.length;
  assert.equal(focusAction(history,'scope','connections'),history);
  assert.equal(focusAction(history,'scope','unknown'),history);
  history=focusAction(history,'search','Ad');
  assert.equal(history.entries.length,length);
  history=focusAction(history,'scope','all');
  history=focusAction(history,'back');
  assert.equal(focusAction(history,'scope','connections'),history);
  assert.equal(historyState(focusAction(history,'forward')).scope,'all');
});

test('scope-only changes form history entries and restore with selection and filters', () => {
  let history=focusAction(initialHistory(),'context','work');
  history=focusAction(history,'select','b');
  history=focusAction(history,'scope','connections');
  assert.equal(history.entries.length,4);
  assert.deepEqual(focusIds(history),['b','c']);
  history=focusAction(history,'scope','all');
  assert.deepEqual(historyState(history),{...fullView,context:'work',selected:'b'});
  assert.deepEqual(focusIds(history),['b','c','e']);
  history=focusAction(history,'back');
  assert.equal(historyState(history).scope,'connections');
  assert.deepEqual(focusIds(history),['b','c']);
  history=focusAction(history,'back');
  assert.equal(historyState(history).scope,'all');
  history=focusAction(history,'forward');
  assert.equal(historyState(history).scope,'connections');
  history=focusAction(history,'search','missing');
  assert.equal(historyState(history).scope,'all');
  assert.equal(focusAction(history,'forward'),history);
  history=focusAction(history,'reset');
  assert.deepEqual(historyState(history),fullView);
  assert.equal(history.entries.length,1);
});

test('focused projection and normalization do not mutate frozen view or state inputs', () => {
  const frozenView=structuredClone(focusView);
  for(const n of frozenView.nodes){Object.freeze(n.spaces);Object.freeze(n);}
  for(const e of frozenView.edges)Object.freeze(e);
  Object.freeze(frozenView.nodes);Object.freeze(frozenView.edges);Object.freeze(frozenView);
  const state={...fullView,categories:Object.freeze([...fullView.categories]),selected:'b',scope:'connections'};Object.freeze(state);
  assert.deepEqual(visibleGraph(frozenView,state).nodes.map(n=>n.id),['a','b','c']);
  const next=reduceState(frozenView,state,{type:'context',value:'personal'});
  assert.equal(next.scope,'all');assert.equal(next.selected,null);
  assert.equal(state.scope,'connections');assert.equal(state.selected,'b');
});


const {shortestPath} = require('../../apps/synthetic_demo/web/path.js');
const route = history => shortestPath(visibleGraph(focusView,historyState(history)),historyState(history).pathStart,historyState(history).pathEnd);

test('endpoint choices join full history without changing selection or scope',()=>{
  let history=focusAction(initialHistory(),'select','c');
  history=focusAction(history,'path-start','a');
  const start=historyState(history);
  history=focusAction(history,'path-end','e');
  const complete=historyState(history);
  assert.deepEqual(complete,{...fullView,selected:'c',pathStart:'a',pathEnd:'e'});
  assert.deepEqual(route(history),{status:'found',nodeIds:['a','c','d','e'],edgeIds:['ac','cd','de']});
  history=focusAction(history,'back');assert.deepEqual(historyState(history),start);
  history=focusAction(history,'forward');assert.deepEqual(historyState(history),complete);
  history=focusAction(history,'clear-path');
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  assert.deepEqual(historyState(focusAction(history,'back')),complete);
});

test('hidden and unknown endpoints and redundant clears preserve Forward',()=>{
  let history=focusAction(initialHistory(),'context','work');
  history=focusAction(history,'path-start','b');
  history=focusAction(history,'path-end','e');
  history=focusAction(history,'back');
  for(const [type,value]of[['path-start','a'],['path-end','unknown'],['path-start','b'],['path-end',null]]) {
    assert.equal(focusAction(history,type,value),history);
  }
  assert.equal(historyState(focusAction(history,'forward')).pathEnd,'e');
  const empty=initialHistory();assert.equal(focusAction(empty,'clear-path'),empty);
});

test('filter changes clear only newly hidden endpoints and Back restores them',()=>{
  for(const [type,value,start,end,expectedStart,expectedEnd]of[
    ['context','work','a','b',null,'b'],
    ['category','journal','a','d','a',null],
    ['search','Ada','a','c',null,'c'],
  ]) {
    let history=focusAction(initialHistory(),'path-start',start);
    history=focusAction(history,'path-end',end);
    const before=historyState(history);
    history=focusAction(history,type,value);
    assert.equal(historyState(history).pathStart,expectedStart);
    assert.equal(historyState(history).pathEnd,expectedEnd);
    assert.deepEqual(historyState(focusAction(history,'back')),before);
  }
});

test('changing the Focus center clears hidden endpoints and Back restores path and center',()=>{
  let history=focusAction(initialHistory(),'select','c');
  history=focusAction(history,'scope','connections');
  history=focusAction(history,'path-start','a');
  history=focusAction(history,'path-end','d');
  const before=historyState(history), beforeRoute=route(history);
  history=focusAction(history,'select','b');
  assert.deepEqual(focusIds(history),['a','b','c']);
  assert.equal(historyState(history).pathStart,'a');
  assert.equal(historyState(history).pathEnd,null);
  assert.equal(route(history).status,'incomplete');
  history=focusAction(history,'back');
  assert.deepEqual(historyState(history),before);assert.deepEqual(route(history),beforeRoute);
  assert.equal(historyState(focusAction(history,'forward')).pathEnd,null);
});

test('entering Focus validates against the new view and Show all never revives hidden choices',()=>{
  let history=focusAction(initialHistory(),'path-start','a');
  history=focusAction(history,'path-end','e');
  history=focusAction(history,'select','b');
  history=focusAction(history,'scope','connections');
  assert.equal(historyState(history).pathStart,'a');assert.equal(historyState(history).pathEnd,null);
  assert.equal(focusAction(history,'path-end','e'),history);
  history=focusAction(history,'scope','all');
  assert.equal(historyState(history).pathEnd,null);
  history=focusAction(history,'path-end','e');assert.equal(route(history).status,'found');
});

test('Show all recomputes over the expanded diagram without changing valid endpoints or filters',()=>{
  const v={nodes:['s','a','b','t','x'].map(id=>({id,label:id,category:'note',spaces:['work']})),edges:[
    {id:'sa',from:'s',to:'a'},{id:'ab',from:'a',to:'b'},{id:'bt',from:'b',to:'t'},
    ...['s','a','b','t'].map(id=>({id:'x'+id,from:'x',to:id}))]};
  let h=reduceHistory(v,initialHistory(),{type:'context',value:'work'});
  h=reduceHistory(v,h,{type:'select',value:'a'});h=reduceHistory(v,h,{type:'scope',value:'connections'});
  h=reduceHistory(v,h,{type:'path-start',value:'s'});h=reduceHistory(v,h,{type:'path-end',value:'b'});
  const before=historyState(h);
  const length=shortestPath(visibleGraph(v,before),'s','b').edgeIds.length;
  h=reduceHistory(v,h,{type:'scope',value:'all'});
  assert.deepEqual(historyState(h),{...before,scope:'all'});
  assert.equal(shortestPath(visibleGraph(v,historyState(h)),'s','b').edgeIds.length,length);
});

test('changed endpoints end search grouping while no-ops preserve it and history branches',()=>{
  let history=action(initialHistory(),'search','a');
  const count=history.entries.length;
  assert.equal(action(history,'path-start','unknown'),history);
  history=action(history,'search','Ad');assert.equal(history.entries.length,count);
  history=action(history,'path-start','c');
  history=action(history,'search','Ada');assert.equal(history.entries.length,count+2);
  history=action(history,'back');history=action(history,'path-end','c');
  assert.equal(action(history,'forward'),history);
  history=action(history,'path-end',null);assert.equal(historyState(history).pathEnd,null);
  history=action(history,'reset');assert.deepEqual(historyState(history),fullView);
  assert.equal(history.entries.length,1);
});

test('endpoint normalization and clearing preserve frozen snapshots',()=>{
  let history=focusAction(initialHistory(),'path-start','a');
  history=focusAction(history,'path-end','d');
  const before=JSON.stringify(history);
  for(const entry of history.entries){Object.freeze(entry.categories);Object.freeze(entry);}
  Object.freeze(history.entries);Object.freeze(history);
  const next=focusAction(history,'category','journal');
  assert.equal(historyState(next).pathEnd,null);
  assert.equal(historyState(next).pathStart,'a');
  assert.equal(historyState(focusAction(history,'clear-path')).pathStart,null);
  assert.equal(JSON.stringify(history),before);
});

const capture = n => ({camera:{x:n,y:-n,scale:1+n/100},
  scroll:{page:{x:0,y:n},list:{x:0,y:n+1},details:{x:0,y:n+2}}});

test('presentation captures are separate from semantic views and defensively copied',()=>{
  assert.equal(typeof rememberPresentation,'function');
  assert.equal(historyPresentation(initialHistory()),null);
  const input=capture(12), history=rememberPresentation(initialHistory(),input);
  assert.deepEqual(historyState(history),fullView);
  assert.deepEqual(historyPresentation(history),input);
  input.camera.x=999;input.scroll.list.y=999;
  const output=historyPresentation(history);output.camera.x=888;output.scroll.page.y=888;
  assert.deepEqual(historyPresentation(history),capture(12));
  assert.equal(history.entries.length,1);assert.equal(history.index,0);assert.equal(history.lastAction,null);
});

test('Back and Forward restore each presentation without populating new semantic steps',()=>{
  let history=rememberPresentation(initialHistory(),capture(10));
  history=action(history,'select','c');assert.equal(historyPresentation(history),null);
  history=rememberPresentation(history,capture(20));
  history=action(history,'context','personal');
  history=rememberPresentation(history,capture(30));
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(20));
  assert.deepEqual(historyState(history),{...fullView,selected:'c'});
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(10));
  history=action(action(history,'forward'),'forward');
  assert.deepEqual(historyPresentation(history),capture(30));
});

test('coalescing clears changed-query capture and collapse restores its predecessor capture',()=>{
  let history=rememberPresentation(initialHistory(),capture(1));
  history=action(history,'search','a');history=rememberPresentation(history,capture(2));
  history=action(history,'search','ad');
  assert.equal(history.entries.length,2);assert.equal(historyPresentation(history),null);
  history=rememberPresentation(history,capture(3));history=action(history,'search','');
  assert.equal(history.entries.length,1);assert.deepEqual(historyPresentation(history),capture(1));
  history=action(history,'search','ada');history=rememberPresentation(history,capture(4));
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(1));
});

test('capture updates preserve Forward, no-op identity and consecutive search grouping',()=>{
  let history=action(initialHistory(),'search','a');
  history=rememberPresentation(history,capture(2));
  assert.equal(action(history,'search','a'),history);
  history=action(history,'search','ad');assert.equal(history.entries.length,2);
  history=action(history,'select','c');history=action(history,'back');
  history=rememberPresentation(history,capture(4));
  assert.equal(history.entries.length,3);assert.equal(history.index,1);
  assert.equal(action(history,'select','unknown'),history);
  assert.equal(historyState(action(history,'forward')).selected,'c');
});

test('presentation alignment survives eviction and branching',()=>{
  let history=initialHistory();
  for(let i=0;i<110;i++) {
    history=rememberPresentation(history,capture(i));
    history=action(history,'select',i%2?'b':'c');
  }
  history=rememberPresentation(history,capture(110));
  assert.equal(history.entries.length,100);assert.equal(history.presentations.length,100);
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(109));
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(108));
  history=action(history,'context','personal');assert.equal(historyPresentation(history),null);
  assert.equal(action(history,'forward'),history);
  history=action(history,'back');assert.deepEqual(historyPresentation(history),capture(108));
});

test('invalid captures preserve history while renderer-free captures remain usable',()=>{
  const history=rememberPresentation(initialHistory(),capture(5));
  for(const bad of [null,{}, {...capture(1),camera:{x:0,y:0,scale:0}},
    {...capture(1),camera:{x:Infinity,y:0,scale:1}},
    {...capture(1),scroll:{...capture(1).scroll,list:{x:0,y:-1}}},
    {...capture(1),scroll:{...capture(1).scroll,page:{x:0,y:NaN}}},
    {...capture(1),camera:{x:'1',y:0,scale:1}}]) assert.equal(rememberPresentation(history,bad),history);
  const withoutRenderer={...capture(7),camera:null};
  assert.deepEqual(historyPresentation(rememberPresentation(history,withoutRenderer)),withoutRenderer);
});

test('capture and navigation preserve frozen inputs and reset clears all presentation history',()=>{
  let history=rememberPresentation(initialHistory(),capture(1));
  history=action(history,'select','c');history=rememberPresentation(history,capture(2));
  const before=JSON.stringify(history);
  const freeze=value=>{if(value&&typeof value==='object'){Object.values(value).forEach(freeze);Object.freeze(value);}};
  freeze(history);const input=capture(3);freeze(input);
  const updated=rememberPresentation(history,input);
  assert.deepEqual(historyPresentation(updated),capture(3));
  assert.equal(JSON.stringify(history),before);
  const reset=action(updated,'reset');assert.equal(historyPresentation(reset),null);
  assert.equal(reset.entries.length,1);assert.equal(reset.presentations.length,1);
});

const {mount}=require('./app_harness.cjs');
const appView={nodes:view.nodes.map(n=>({...n,description:'Fictional',degree:2,x:50,y:60})),edges:view.edges};

test('app Back and Forward restore map and all scroll targets after DOM rebuilding',()=>{
  const app=mount(appView);
  app.select('c');app.setPresentation(capture(10));
  app.select('b');app.setPresentation(capture(20));
  app.click('history-back');assert.deepEqual(app.presentation(),capture(10));
  assert.equal(app.nodes.get('node-label').textContent,'Ada');
  app.click('history-forward');assert.deepEqual(app.presentation(),capture(20));
  assert.equal(app.nodes.get('node-label').textContent,'Project Lighthouse');
  assert.equal(app.document.activeElement.id,'history-back');
});

test('app restoration survives pending focus animation and a late initial draw',()=>{
  const app=mount(appView,{draw:false});app.setPresentation(capture(15));
  app.select('b');
  app.click('history-back');app.network.finishAnimation();app.network.emit('afterDrawing');
  assert.deepEqual(app.presentation(),capture(15));
});

test('app-owned focus never schedules an uncancellable first-frame animation',()=>{
  const app=mount(appView);app.select('b');
  assert.equal(app.network.focuses[0].animation,false);
  assert.equal(app.network.pending,null);
});

test('app search collapse restores predecessor camera/scroll before a fresh search',()=>{
  const app=mount(appView);app.setPresentation(capture(5));
  app.search('a');app.setPresentation(capture(9));app.search('');
  assert.deepEqual(app.presentation(),capture(5));
  app.search('ad');app.setPresentation(capture(12));app.click('history-back');
  assert.deepEqual(app.presentation(),capture(5));
  app.click('history-forward');assert.deepEqual(app.presentation(),capture(12));
});

test('app no-op endpoint actions preserve scroll and Forward without rebuilding',()=>{
  const app=mount(appView);app.select('b');app.select('c');app.click('history-back');
  app.setPresentation(capture(8));const before=app.nodes.get('node-list').rebuilds;
  app.nodes.get('path-start').value='';app.nodes.get('path-start').emit('change');
  assert.equal(app.nodes.get('node-list').rebuilds,before);
  assert.deepEqual(app.presentation(),capture(8));
  app.click('history-forward');app.click('history-back');
  assert.deepEqual(app.presentation(),capture(8));
});

test('app preserves renderer-free scroll and clamps restored positions after reflow',()=>{
  const app=mount(appView,{renderer:false});app.setPresentation({...capture(15),camera:null});
  app.select('b');app.page.maxScroll=5;app.nodes.get('node-list').maxScroll=6;
  app.click('history-back');
  assert.deepEqual(app.presentation(),{camera:null,scroll:{page:{x:0,y:5},list:{x:0,y:6},details:{x:0,y:17}}});
});

test('map and scroll interactions create no navigation steps or Forward truncation',()=>{
  const app=mount(appView);app.select('b');app.select('c');app.click('history-back');
  const position=app.nodes.get('history-position').textContent;
  app.setPresentation(capture(7));app.scroll();app.network.emit('zoom');app.network.emit('dragEnd');
  assert.equal(app.nodes.get('history-position').textContent,position);
  assert.equal(app.nodes.get('history-forward').disabled,false);
  app.click('history-forward');app.click('history-back');assert.deepEqual(app.presentation(),capture(7));
});

test('explicit reselection recenters without adding a step or discarding Forward',()=>{
  const app=mount(appView);app.select('b');app.select('c');app.click('history-back');
  app.setPresentation(capture(8));const before=app.nodes.get('history-position').textContent;
  app.select('b');assert.equal(app.nodes.get('history-position').textContent,before);
  assert.equal(app.nodes.get('history-forward').disabled,false);
  assert.deepEqual(app.network.camera,{x:50,y:60,scale:1.08});
  app.click('history-forward');app.click('history-back');
  assert.deepEqual(app.network.camera,{x:50,y:60,scale:1.08});
});

test('selected endpoint shortcuts set the right targets without moving the camera',()=>{
  const app=mount(appView);
  assert.equal(app.nodes.get('use-selected-start').disabled,true);
  assert.equal(app.nodes.get('use-selected-end').disabled,true);
  app.select('b');app.setPresentation(capture(12));
  app.click('use-selected-start');
  assert.equal(app.nodes.get('path-start').value,'b');
  assert.equal(app.nodes.get('path-end').value,'');
  assert.deepEqual(app.network.camera,capture(12).camera);
  assert.equal(app.nodes.get('history-position').textContent,'3 / 3');
  app.select('c');app.setPresentation(capture(18));app.click('use-selected-end');
  assert.equal(app.nodes.get('path-start').value,'b');
  assert.equal(app.nodes.get('path-end').value,'c');
  assert.deepEqual(app.network.camera,capture(18).camera);
  assert.equal(app.document.activeElement.id,'use-selected-end');
});

test('duplicate selected endpoint after Back preserves Forward, capture and control focus',()=>{
  const app=mount(appView);app.select('b');app.click('use-selected-start');
  assert.equal(app.nodes.get('path-start').value,'b');
  app.select('c');app.click('history-back');app.setPresentation(capture(27));
  const position=app.nodes.get('history-position').textContent;
  const rebuilds=app.nodes.get('node-list').rebuilds;
  app.click('use-selected-start');
  assert.equal(app.nodes.get('history-position').textContent,position);
  assert.equal(app.nodes.get('history-forward').disabled,false);
  assert.equal(app.nodes.get('node-list').rebuilds,rebuilds);
  assert.equal(app.document.activeElement.id,'use-selected-start');
  assert.deepEqual(app.presentation(),capture(27));
  app.click('history-forward');assert.equal(app.nodes.get('node-label').textContent,'Ada');
  app.click('history-back');assert.deepEqual(app.presentation(),capture(27));
});

test('duplicate selected endpoint keeps consecutive search typing in one history step',()=>{
  const app=mount(appView);app.select('c');app.click('use-selected-start');
  app.search('a');const position=app.nodes.get('history-position').textContent;
  app.click('use-selected-start');app.search('ad');
  assert.equal(app.nodes.get('history-position').textContent,position);
  app.click('history-back');assert.equal(app.nodes.get('search').value,'');
  assert.equal(app.nodes.get('path-start').value,'c');
});

test('selected endpoint shortcuts preserve Focus and perspective while history restores endpoints',()=>{
  const app=mount(appView);app.select('b');
  app.contexts.find(b=>b.dataset.context==='work').emit('click');
  app.click('focus-connections');app.click('use-selected-start');app.select('c');
  app.setPresentation(capture(11));app.click('use-selected-end');
  assert.equal(app.nodes.get('focus-connections').attributes['aria-pressed'],'true');
  assert.equal(app.nodes.get('view-title').textContent,'The work perspective');
  assert.equal(app.nodes.get('path-start').value,'b');assert.equal(app.nodes.get('path-end').value,'c');
  assert.deepEqual(app.network.camera,capture(11).camera);
  app.click('history-back');assert.equal(app.nodes.get('path-end').value,'');
  app.click('history-forward');assert.equal(app.nodes.get('path-end').value,'c');
  assert.deepEqual(app.network.camera,capture(11).camera);
});

test('hidden and empty selections disable both shortcuts without adding history',()=>{
  const app=mount(appView);app.select('b');app.click('use-selected-start');
  app.contexts.find(b=>b.dataset.context==='personal').emit('click');
  assert.equal(app.nodes.get('use-selected-start').disabled,true);
  assert.equal(app.nodes.get('use-selected-end').disabled,true);
  assert.equal(app.nodes.get('path-start').value,'');
  assert.equal(app.nodes.get('path-selected-hint').textContent,'Select a page on the map or in the list first.');
  app.search('fictional-no-results');const position=app.nodes.get('history-position').textContent;
  assert.equal(app.nodes.get('path-selected-hint').textContent,'No pages in this view. Change or reset filters, then select a page.');
  app.click('use-selected-end');assert.equal(app.nodes.get('history-position').textContent,position);
  app.click('reset');assert.equal(app.nodes.get('history-position').textContent,'1 / 1');
  assert.equal(app.nodes.get('use-selected-start').disabled,true);
});

test('selected-page hint retains hostile fictional labels as literal text',()=>{
  const hostile='</script><img src=x onerror=alert(1)>';
  const data={...appView,nodes:appView.nodes.map(n=>n.id==='b'?{...n,label:hostile}:n)};
  const app=mount(data);app.select('b');
  assert.equal(app.nodes.get('path-selected-hint').textContent,'Selected page: '+hostile);
  assert.equal(app.nodes.get('path-selected-hint').children.length,0);
  app.click('use-selected-end');assert.equal(app.nodes.get('path-end').value,'b');
});
