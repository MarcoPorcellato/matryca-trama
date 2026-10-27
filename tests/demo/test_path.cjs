const test = require('node:test');
const assert = require('node:assert/strict');
const { shortestPath } = require('../../apps/synthetic_demo/web/path.js');
const graph = {nodes:['s','a','b','c','t','alone'].map(id=>({id})),edges:[
  {id:'sc',from:'s',to:'c'},{id:'cb',from:'c',to:'b'},{id:'bt',from:'b',to:'t'},
  {id:'sa',from:'s',to:'a'},{id:'at',from:'a',to:'t'}]};

test('a route minimizes link count instead of following the first longer branch',()=>{
  assert.deepEqual(shortestPath(graph,'s','t'),{status:'found',nodeIds:['s','a','t'],edgeIds:['sa','at']});
});
test('links can be traversed in either direction',()=>{
  assert.deepEqual(shortestPath(graph,'t','s'),{status:'found',nodeIds:['t','a','s'],edgeIds:['at','sa']});
});
test('equal paths use node-ID order independent of input ordering',()=>{
  const tied={nodes:[{id:'s'},{id:'b'},{id:'a'},{id:'t'}],edges:[
    {id:'sb',from:'s',to:'b'},{id:'bt',from:'b',to:'t'},
    {id:'sa',from:'s',to:'a'},{id:'at',from:'a',to:'t'}]};
  const expected={status:'found',nodeIds:['s','a','t'],edgeIds:['sa','at']};
  assert.deepEqual(shortestPath(tied,'s','t'),expected);
  assert.deepEqual(shortestPath({nodes:[...tied.nodes].reverse(),edges:[...tied.edges].reverse()},'s','t'),expected);
});
test('parallel links use edge-ID order even when their directions differ',()=>{
  const parallel={nodes:[{id:'s'},{id:'a'}],edges:[{id:'z',from:'s',to:'a'},{id:'a',from:'a',to:'s'}]};
  assert.deepEqual(shortestPath(parallel,'s','a'),{status:'found',nodeIds:['s','a'],edgeIds:['a']});
});
test('identical valid endpoints have a zero-link path',()=>{
  assert.deepEqual(shortestPath(graph,'alone','alone'),{status:'found',nodeIds:['alone'],edgeIds:[]});
});
test('disconnected valid endpoints are distinct from incomplete choices',()=>{
  assert.deepEqual(shortestPath(graph,'s','alone'),{status:'unreachable',nodeIds:[],edgeIds:[]});
  for(const [start,end]of[[null,'s'],['s',null],['unknown','t'],['s','unknown']]){
    assert.deepEqual(shortestPath(graph,start,end),{status:'incomplete',nodeIds:[],edgeIds:[]});
  }
});
test('dangling edges and cycles do not invent or repeat nodes',()=>{
  const cyclic={nodes:[{id:'a'},{id:'b'},{id:'c'}],edges:[
    {id:'outside',from:'a',to:'hidden'},{id:'aa',from:'a',to:'a'},
    {id:'ab',from:'a',to:'b'},{id:'ba',from:'b',to:'a'},{id:'bc',from:'b',to:'c'}]};
  assert.deepEqual(shortestPath(cyclic,'a','c'),{status:'found',nodeIds:['a','b','c'],edgeIds:['ab','bc']});
});
test('path projection leaves frozen input arrays and values untouched',()=>{
  const frozen=structuredClone(graph);
  frozen.nodes.forEach(Object.freeze);frozen.edges.forEach(Object.freeze);
  Object.freeze(frozen.nodes);Object.freeze(frozen.edges);Object.freeze(frozen);
  const before=JSON.stringify(frozen);
  assert.deepEqual(shortestPath(frozen,'s','t'),{status:'found',nodeIds:['s','a','t'],edgeIds:['sa','at']});
  assert.equal(JSON.stringify(frozen),before);
});
