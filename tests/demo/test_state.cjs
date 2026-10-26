const test = require('node:test');
const assert = require('node:assert/strict');
const { initialState, reduceState, visibleGraph, neighbors, suggestedNode } = require('../../apps/synthetic_demo/web/state.js');
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
