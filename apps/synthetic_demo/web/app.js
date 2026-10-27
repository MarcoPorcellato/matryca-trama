/* Trama presentation composition over the local fictional view and renderer. */
(function () {
  'use strict';
  const view = JSON.parse(document.getElementById('demo-data').textContent);
  const { initialHistory, historyState, reduceHistory, visibleGraph, neighbors, suggestedNode } = window.TramaDemoState;
  const categories = { note:['Note','#78dfbb'],project:['Project','#b5a0fc'],journal:['Journal','#7bb5fa'],tag:['Tag','#e6c17a'] };
  const byId = new Map(view.nodes.map(n => [n.id,n]));
  const $ = id => document.getElementById(id);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let history = initialHistory();
  let state = historyState(history);
  let network = null, graphNodes = null, graphEdges = null;
  function element(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  if (window.vis && window.vis.Network && window.vis.DataSet) {
    graphNodes = new window.vis.DataSet(view.nodes.map(n => ({
      id:n.id,label:n.label,x:n.x,y:n.y,shape:'dot',size:9+Math.sqrt(n.degree)*3,
      title:element('span','',n.label),borderWidth:1.4,
      color:{background:categories[n.category][1],border:categories[n.category][1],
        highlight:{background:categories[n.category][1],border:'#f2fff8'},hover:{background:categories[n.category][1],border:'#e4fff1'}},
    })));
    graphEdges = new window.vis.DataSet(view.edges.map(e => ({...e})));
    network = new window.vis.Network($('graph'), {nodes:graphNodes,edges:graphEdges}, {
      autoResize:true,layout:{randomSeed:42},physics:false,
      nodes:{font:{size:13,color:'#bfced7',face:'system-ui',strokeWidth:3,strokeColor:'#0d1722'}},
      edges:{width:1,color:{color:'#365363',highlight:'#9adfc8',hover:'#6e9d94'},smooth:false,selectionWidth:2},
      interaction:{hover:true,tooltipDelay:250,keyboard:false,zoomView:true,dragView:true,multiselect:false},
    });
    network.on('click', event => { if (event.nodes.length) dispatch({type:'select',value:event.nodes[0]},false); });
    network.once('afterDrawing', () => fit());
  }
  function fit() {
    if (!network) return;
    const ids = visibleGraph(view,state).nodes.map(n=>n.id);
    if (!ids.length) return;
    network.fit({nodes:ids,animation:false});
    if (network.getScale()>1.15) network.moveTo({scale:1.15,animation:false});
  }
  function zoom(factor) {
    if (network) network.moveTo({scale:Math.max(.15,Math.min(3,network.getScale()*factor)),animation:false});
  }
  function nodeButton(node, selected, neighbor) {
    const button = element('button','node-row'+(selected?' is-selected':''));
    button.type='button';button.dataset.nodeId=node.id;
    button.setAttribute('aria-pressed',String(selected));
    button.append(element('i','dot '+node.category),element('span','node-name',node.label),element('small','',neighbor?'↗':String(node.degree)));
    button.addEventListener('click',()=>dispatch({type:'select',value:node.id},true));
    return button;
  }
  function countLabel(count, singular) {
    return count+' '+singular+(count===1?'':'s');
  }
  function render() {
    const current = visibleGraph(view,state);
    const ids = new Set(current.nodes.map(n=>n.id));
    const focused = document.activeElement && (document.activeElement.dataset.nodeId
      || (document.activeElement.id === 'start-exploring' ? state.selected : null));
    $('history-back').disabled=history.index===0;
    $('history-forward').disabled=history.index===history.entries.length-1;
    $('history-position').textContent=(history.index+1)+' / '+history.entries.length;
    $('history-position').setAttribute('aria-label','Step '+(history.index+1)+' of '+history.entries.length);
    $('node-count').textContent=current.nodes.length;$('edge-count').textContent=current.edges.length;
    $('list-count').textContent=countLabel(current.nodes.length,'node');
    $('view-title').textContent={all:'The whole picture',work:'The work perspective',personal:'The personal perspective'}[state.context];
    $('empty').hidden=current.nodes.length!==0;
    $('search').value=state.query;
    document.querySelectorAll('[data-context]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.context===state.context)));
    document.querySelectorAll('[data-category]').forEach(b=>{b.checked=state.categories.includes(b.dataset.category);});
    $('node-list').replaceChildren(...current.nodes.map(n=>nodeButton(n,n.id===state.selected,false)));
    if (!current.nodes.length) $('node-list').append(element('p','no-neighbors','No results. Try a different filter.'));
    if (network) {
      graphNodes.update(view.nodes.map(n=>({id:n.id,hidden:!ids.has(n.id)})));
      graphEdges.update(view.edges.map(e=>({id:e.id,hidden:!ids.has(e.from)||!ids.has(e.to)})));
      if (state.selected) network.selectNodes([state.selected]);else network.unselectAll();
    }
    const node = byId.get(state.selected);
    $('focus-connections').disabled=!node;
    $('focus-connections').setAttribute('aria-pressed',String(state.scope==='connections'));
    $('show-all').disabled=state.scope!=='connections';
    $('scope-description').textContent=!node
      ? (current.nodes.length?'Select a node on the map or in the list first.':'No nodes match. Change or reset filters, then select a node.')
      : state.scope==='connections'?'Connections of '+node.label:'All nodes matching your filters';
    $('inspector-empty').hidden=Boolean(node);$('details').hidden=!node;
    const suggestion=suggestedNode(view,state);
    $('start-exploring').disabled=!suggestion;
    $('start-exploring').dataset.suggested=suggestion?suggestion.id:'';
    $('start-exploring').textContent=suggestion?'Explore '+suggestion.label:'Change the filters';
    if (suggestion) $('start-exploring').append(element('span','','→'));
    if (node) {
      $('node-label').textContent=node.label;$('node-description').textContent=node.description;
      $('node-category').textContent=categories[node.category][0];$('node-category').style.color=categories[node.category][1];
      $('node-spaces').replaceChildren(...node.spaces.map(s=>element('span','',s==='work'?'Work':'Personal')));
      const adjacent = neighbors(current,node.id);
      $('neighbor-count').textContent=adjacent.length;
      $('neighbors').replaceChildren(...adjacent.map(id=>nodeButton(byId.get(id),false,true)));
      if (!adjacent.length) $('neighbors').append(element('p','no-neighbors',state.scope==='connections'?'No visible neighbors. Use Show all to explore other nodes.':'No visible neighbors. Change the filters or explore another node.'));
    }
    $('status').textContent=countLabel(current.nodes.length,'node')+' and '+countLabel(current.edges.length,'link')+' visible'+(node?'. Selected: '+node.label:'')+'. Step '+(history.index+1)+' of '+history.entries.length+(state.scope==='connections'?'. Focused connections':'. All matching nodes');
    if (focused && ids.has(focused)) {
      const button = Array.from($('node-list').querySelectorAll('button')).find(b=>b.dataset.nodeId===focused);
      if (button) button.focus({preventScroll:true});
    }
  }
  function dispatch(action, focus) {
    const focusedControl = document.activeElement && document.activeElement.id;
    const next = reduceHistory(view,history,action);
    const reselecting = focus && action.type === 'select' && action.value === state.selected;
    if (next === history && !reselecting) return;
    history=next;state=historyState(history);render();
    const traveling = action.type === 'back' || action.type === 'forward';
    if (state.scope === 'connections') {
      fit();
    } else {
      if ((focus || traveling) && state.selected && network) network.focus(state.selected,{scale:Math.max(.85,network.getScale()),animation:reduced?false:{duration:250,easingFunction:'easeInOutQuad'}});
      if ((traveling && !state.selected) || ['context','category','reset','scope'].includes(action.type)) fit();
    }
    if (focusedControl === 'show-all' && $('show-all').disabled) {
      ($('focus-connections').disabled ? $('reset') : $('focus-connections')).focus({preventScroll:true});
    }
    if (traveling && ['history-back','history-forward'].includes(focusedControl) && $(focusedControl).disabled) {
      const opposite = $(focusedControl === 'history-back' ? 'history-forward' : 'history-back');
      (opposite.disabled ? $('reset') : opposite).focus({preventScroll:true});
    }
  }
  $('search').addEventListener('input',event=>dispatch({type:'search',value:event.target.value},false));
  document.querySelectorAll('[data-context]').forEach(b=>b.addEventListener('click',()=>dispatch({type:'context',value:b.dataset.context},false)));
  document.querySelectorAll('[data-category]').forEach(b=>b.addEventListener('change',()=>dispatch({type:'category',value:b.dataset.category},false)));
  $('focus-connections').addEventListener('click',()=>dispatch({type:'scope',value:'connections'},false));
  $('show-all').addEventListener('click',()=>dispatch({type:'scope',value:'all'},false));
  $('history-back').addEventListener('click',()=>dispatch({type:'back'},false));
  $('history-forward').addEventListener('click',()=>dispatch({type:'forward'},false));
  $('reset').addEventListener('click',()=>dispatch({type:'reset'},false));
  $('start-exploring').addEventListener('click',()=>dispatch({type:'select',value:$('start-exploring').dataset.suggested},true));
  $('zoom-in').addEventListener('click',()=>zoom(1.25));$('zoom-out').addEventListener('click',()=>zoom(.8));$('fit').addEventListener('click',fit);
  $('credits-open').addEventListener('click',()=>$('credits').showModal());
  $('credits-close').addEventListener('click',()=>$('credits').close());
  render();
})();
