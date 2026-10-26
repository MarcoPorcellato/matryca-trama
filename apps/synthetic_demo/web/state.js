/* Pure presentation state. No source transport, storage or DOM access. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TramaDemoState = api;
})(globalThis, function () {
  'use strict';
  const categories = ['note', 'project', 'journal', 'tag'];
  const normalized = value => String(value).normalize('NFD').replace(/\p{M}/gu, '').toLocaleLowerCase('it').trim();
  function initialState() { return { query: '', context: 'all', categories: [...categories], selected: null }; }
  function visibleGraph(view, state) {
    const query = normalized(state.query);
    const nodes = view.nodes.filter(n => state.categories.includes(n.category)
      && (state.context === 'all' || n.spaces.includes(state.context))
      && normalized(n.label).includes(query));
    const ids = new Set(nodes.map(n => n.id));
    return { nodes, edges: view.edges.filter(e => ids.has(e.from) && ids.has(e.to)) };
  }
  function reduceState(view, old, action) {
    if (action.type === 'reset') return initialState();
    const state = { ...old, categories: [...old.categories] };
    if (action.type === 'search') state.query = String(action.value);
    if (action.type === 'context' && ['all','work','personal'].includes(action.value)) state.context = action.value;
    if (action.type === 'category' && categories.includes(action.value)) {
      state.categories = state.categories.includes(action.value)
        ? state.categories.filter(c => c !== action.value) : [...state.categories, action.value];
    }
    if (action.type === 'select') state.selected = action.value;
    if (!visibleGraph(view, state).nodes.some(n => n.id === state.selected)) state.selected = null;
    return state;
  }
  function neighbors(view, id) {
    const ids = new Set(view.edges.flatMap(e => e.from === id ? [e.to] : e.to === id ? [e.from] : []));
    return view.nodes.filter(n => ids.has(n.id)).map(n => n.id);
  }
  function suggestedNode(view, state) {
    const visible = visibleGraph(view,state).nodes;
    return visible.find(n=>n.category==='project') || visible[0] || null;
  }
  return { initialState, reduceState, visibleGraph, neighbors, suggestedNode };
});
