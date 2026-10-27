const test = require('node:test');
const assert = require('node:assert/strict');
const { initialState, reduceState, visibleGraph, neighbors, suggestedNode, filteredGraph, initialHistory, historyState, reduceHistory } = require('../../apps/synthetic_demo/web/state.js');
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

const fullView = {query:'',context:'all',categories:['note','project','journal','tag'],selected:null,scope:'all'};
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
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null,scope:'all'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'c'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'b'});
  history=action(action(action(history,'forward'),'forward'),'forward');
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null,scope:'all'});
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
