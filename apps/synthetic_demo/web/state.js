/* Pure presentation state. No source transport, storage or DOM access. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TramaDemoState = api;
})(globalThis, function () {
  'use strict';
  const categories = ['note', 'project', 'journal', 'tag'];
  const normalized = value => String(value).normalize('NFD').replace(/\p{M}/gu, '').toLocaleLowerCase('en').trim();
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
    if (action.type === 'select' && visibleGraph(view,state).nodes.some(n=>n.id===action.value)) {
      state.selected = action.value;
    }
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
  function initialHistory() {
    return { entries: [initialState()], index: 0, lastAction: null };
  }
  function historyState(history) {
    return history.entries[history.index];
  }
  function sameView(left, right) {
    return left.query === right.query && left.context === right.context
      && left.selected === right.selected
      && left.categories.length === right.categories.length
      && left.categories.every(category => right.categories.includes(category));
  }
  function reduceHistory(view, history, action) {
    if (action.type === 'reset') return initialHistory();
    if (action.type === 'back' || action.type === 'forward') {
      const index = history.index + (action.type === 'back' ? -1 : 1);
      if (index < 0 || index >= history.entries.length) return history;
      return { ...history, index, lastAction: null };
    }
    const next = reduceState(view, historyState(history), action);
    if (sameView(next, historyState(history))) return history;
    const entries = history.entries.slice(0, history.index + 1);
    const coalesce = action.type === 'search' && history.lastAction === 'search'
      && history.index === history.entries.length - 1 && history.index > 0;
    if (coalesce) {
      if (sameView(next, entries[entries.length - 2])) {
        entries.pop();
        return { entries, index: entries.length - 1, lastAction: null };
      }
      entries[entries.length - 1] = next;
    } else {
      entries.push(next);
    }
    const bounded = entries.slice(-100);
    return { entries: bounded, index: bounded.length - 1, lastAction: action.type };
  }
  return { initialState, reduceState, visibleGraph, neighbors, suggestedNode,
    initialHistory, historyState, reduceHistory };
});
