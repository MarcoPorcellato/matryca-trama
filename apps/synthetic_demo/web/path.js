/* Shortest route through the already-visible fictional diagram. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TramaDemoPath = api;
})(globalThis, function () {
  'use strict';
  const compare = (left, right) => left < right ? -1 : left > right ? 1 : 0;
  function shortestPath(view, startId, endId) {
    const adjacent = new Map(view.nodes.map(node => [node.id, []]));
    if (!adjacent.has(startId) || !adjacent.has(endId)) {
      return {status:'incomplete', nodeIds:[], edgeIds:[]};
    }
    for (const edge of view.edges) {
      if (!adjacent.has(edge.from) || !adjacent.has(edge.to)) continue;
      adjacent.get(edge.from).push({nodeId:edge.to, edgeId:edge.id});
      adjacent.get(edge.to).push({nodeId:edge.from, edgeId:edge.id});
    }
    for (const links of adjacent.values()) {
      links.sort((a, b) => compare(a.nodeId, b.nodeId) || compare(a.edgeId, b.edgeId));
    }
    const parents = new Map([[startId, null]]);
    const queue = [startId];
    for (let index = 0; index < queue.length && !parents.has(endId); index++) {
      const current = queue[index];
      for (const link of adjacent.get(current)) {
        if (parents.has(link.nodeId)) continue;
        parents.set(link.nodeId, {nodeId:current, edgeId:link.edgeId});
        queue.push(link.nodeId);
      }
    }
    if (!parents.has(endId)) return {status:'unreachable', nodeIds:[], edgeIds:[]};
    const nodeIds = [], edgeIds = [];
    for (let current = endId; current !== null;) {
      nodeIds.push(current);
      const parent = parents.get(current);
      if (parent) edgeIds.push(parent.edgeId);
      current = parent ? parent.nodeId : null;
    }
    return {status:'found', nodeIds:nodeIds.reverse(), edgeIds:edgeIds.reverse()};
  }
  return {shortestPath};
});
