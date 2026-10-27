const test = require('node:test');
const assert = require('node:assert/strict');
const { initialState, reduceState, visibleGraph, neighbors, suggestedNode, initialHistory, historyState, reduceHistory } = require('../../apps/synthetic_demo/web/state.js');
const view = { nodes: [
  {id:'a',label:'Caffè e idee',category:'note',spaces:['personal']},
  {id:'b',label:'Progetto Faro',category:'project',spaces:['work']},
  {id:'c',label:'Ada',category:'note',spaces:['personal','work']},
  {id:'d',label:'Diario',category:'journal',spaces:['personal']},
], edges:[{id:'ab',from:'a',to:'b'},{id:'bc',from:'b',to:'c'},{id:'cd',from:'c',to:'d'}] };
test('search is case and accent insensitive', () => {
  const state = reduceState(view, initialState(), {type:'search',value:'CAFFE'});
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

const fullView = {query:'',context:'all',categories:['note','project','journal','tag'],selected:null};
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
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal',selected:'c'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,context:'personal'});
  history=action(history,'back');
  assert.deepEqual(historyState(history),{...fullView,selected:'b'});
  history=action(action(action(history,'forward'),'forward'),'forward');
  assert.deepEqual(historyState(history),{query:'',context:'personal',categories:['project','journal','tag'],selected:null});
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
  for(const query of ['C','Ca','Caf','CAFFE'])history=action(history,'search',query);
  assert.equal(history.entries.length,2);
  history=action(history,'back');
  assert.deepEqual(historyState(history),fullView);
  history=action(history,'forward');
  assert.deepEqual(historyState(history),{...fullView,query:'CAFFE'});
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
