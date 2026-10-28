/* Trama presentation composition over the local fictional view and renderer. */
(function () {
  'use strict';
  const view = JSON.parse(document.getElementById('demo-data').textContent);
  const { initialHistory, historyState, reduceHistory, historyPresentation, rememberPresentation,
    visibleGraph, neighbors, suggestedNode } = window.TramaDemoState;
  const { shortestPath } = window.TramaDemoPath;
  const categories = { note:['Note','#78dfbb'],project:['Project','#b5a0fc'],journal:['Journal','#7bb5fa'],tag:['Tag','#e6c17a'] };
  const byId = new Map(view.nodes.map(n => [n.id,n]));
  const $ = id => document.getElementById(id);
  let history = initialHistory();
  let state = historyState(history);
  let network = null, graphNodes = null, graphEdges = null;
  let presenting = false, initialFitPending = true;
  function scrollTargets() {
    return {page:document.scrollingElement,list:$('node-list'),details:$('details')};
  }
  function capturePresentation() {
    const position = network && network.getViewPosition();
    return {camera:position ? {x:position.x,y:position.y,scale:network.getScale()} : null,
      scroll:Object.fromEntries(Object.entries(scrollTargets()).map(([key,node])=>
        [key,{x:Math.max(0,node.scrollLeft),y:Math.max(0,node.scrollTop)}]))};
  }
  function rememberCurrentPresentation() {
    if (!presenting) history=rememberPresentation(history,capturePresentation());
  }
  function restorePresentation(snapshot) {
    if (network && snapshot.camera) network.moveTo({
      position:{x:snapshot.camera.x,y:snapshot.camera.y},scale:snapshot.camera.scale,animation:false});
    for (const [key,node] of Object.entries(scrollTargets())) {
      node.scrollLeft=snapshot.scroll[key].x;node.scrollTop=snapshot.scroll[key].y;
    }
  }
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
    network.once('afterDrawing', () => { if (initialFitPending) fit(); });
    for (const event of ['zoom','dragEnd','animationFinished']) network.on(event,rememberCurrentPresentation);
  }
  function fit() {
    initialFitPending=false;
    if (!network) return;
    const ids = visibleGraph(view,state).nodes.map(n=>n.id);
    if (!ids.length) return;
    network.fit({nodes:ids,animation:false});
    if (network.getScale()>1.15) network.moveTo({scale:1.15,animation:false});
    rememberCurrentPresentation();
  }
  function zoom(factor) {
    initialFitPending=false;
    if (network) network.moveTo({scale:Math.max(.15,Math.min(3,network.getScale()*factor)),animation:false});
    rememberCurrentPresentation();
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
  function renderPath(current, path) {
    const selected = current.nodes.find(node=>node.id===state.selected);
    $('use-selected-start').disabled=!selected;$('use-selected-end').disabled=!selected;
    $('path-selected-hint').textContent=selected ? 'Selected page: '+selected.label
      : current.nodes.length ? 'Select a page on the map or in the list first.'
      : 'No pages in this view. Change or reset filters, then select a page.';
    for (const [id, value] of [['path-start',state.pathStart],['path-end',state.pathEnd]]) {
      const placeholder = element('option','',current.nodes.length?'Choose a page…':'No pages in this view');
      placeholder.value='';
      $(id).replaceChildren(placeholder,...current.nodes.map(node=>{
        const option=element('option','',node.label);option.value=node.id;return option;
      }));
      $(id).value=value || '';$(id).disabled=!current.nodes.length;
    }
    $('clear-path').disabled=!state.pathStart && !state.pathEnd;
    $('path-scope').textContent=state.scope==='connections'
      ? 'Focus connections limits the route. Show all widens the view and keeps your search and filters.'
      : 'Search and filters limit the route, including every intermediate page.';
    let result='Choose a start and an end page.', summary='Choose two pages';
    if (!current.nodes.length) {
      result='No pages in this view. Change or reset filters to find a path.';summary='No pages in this view';
    } else if (path.status==='found') {
      result=path.edgeIds.length ? 'Shortest path in this view: '+countLabel(path.edgeIds.length,'link')+'.' : 'Same page: 0 links.';
      summary=countLabel(path.edgeIds.length,'link')+' · '+countLabel(path.nodeIds.length,'page')+' highlighted';
    } else if (path.status==='unreachable') {
      result='No path in this view. '+(state.scope==='connections'?'Try Show all or change filters.':'Change filters to explore another view.');
      summary='No path in this view';
    } else if (state.pathStart || state.pathEnd) {
      result=state.pathStart?'Choose an end page.':'Choose a start page.';summary='Choose one more page';
    }
    $('path-summary').textContent=summary;$('path-result').textContent=result;
    $('path-steps').replaceChildren(...path.nodeIds.map(id=>element('li','',byId.get(id).label)));
    $('path-steps').hidden=path.status!=='found';
  }
  function render() {
    const current = visibleGraph(view,state);
    const path = shortestPath(current,state.pathStart,state.pathEnd);
    const pathNodes = new Set(path.nodeIds), pathEdges = new Set(path.edgeIds);
    renderPath(current,path);
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
      graphNodes.update(view.nodes.map(n=>{
        const onPath=pathNodes.has(n.id), color=categories[n.category][1];
        return {id:n.id,hidden:!ids.has(n.id),borderWidth:onPath?3:1.4,
          font:{color:onPath?'#ffe5ab':'#bfced7'},
          color:{background:color,border:onPath?'#ffd68a':color,
            highlight:{background:color,border:onPath?'#ffd68a':'#f2fff8'},
            hover:{background:color,border:onPath?'#ffd68a':'#e4fff1'}}};
      }));
      graphEdges.update(view.edges.map(e=>{
        const onPath=pathEdges.has(e.id);
        return {id:e.id,hidden:!ids.has(e.from)||!ids.has(e.to),width:onPath?3:1,
          color:{color:onPath?'#ffd68a':'#365363',highlight:onPath?'#ffd68a':'#9adfc8',hover:onPath?'#ffd68a':'#6e9d94'}};
      }));
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
    const captured = rememberPresentation(history,capturePresentation());
    const next = reduceHistory(view,captured,action);
    const reselecting = focus && action.type === 'select' && action.value === state.selected;
    history=captured;
    if (next === captured && !reselecting) return;
    const traveling = action.type === 'back' || action.type === 'forward';
    const restoring = traveling || (action.type === 'search' && next.index < captured.index);
    const destination = restoring ? historyPresentation(next) : null;
    initialFitPending=false;presenting=true;
    history=next;state=historyState(history);render();
    const pathAction = ['path-start','path-end','clear-path'].includes(action.type);
    if (!destination && !pathAction && state.scope === 'connections') {
      fit();
    } else if (!destination && !pathAction) {
      if ((focus || traveling) && state.selected && network) network.focus(state.selected,{scale:Math.max(.85,network.getScale()),animation:false});
      if ((traveling && !state.selected) || ['context','category','reset','scope'].includes(action.type)) fit();
    }
    if (focusedControl === 'show-all' && $('show-all').disabled) {
      ($('focus-connections').disabled ? $('reset') : $('focus-connections')).focus({preventScroll:true});
    }
    if (focusedControl === 'clear-path' && $('clear-path').disabled) {
      ($('path-start').disabled ? $('reset') : $('path-start')).focus({preventScroll:true});
    }
    if (traveling && ['history-back','history-forward'].includes(focusedControl) && $(focusedControl).disabled) {
      const opposite = $(focusedControl === 'history-back' ? 'history-forward' : 'history-back');
      (opposite.disabled ? $('reset') : opposite).focus({preventScroll:true});
    }
    if (destination) restorePresentation(destination);
    presenting=false;rememberCurrentPresentation();
  }
  document.addEventListener('scroll',rememberCurrentPresentation,true);
  $('search').addEventListener('input',event=>dispatch({type:'search',value:event.target.value},false));
  document.querySelectorAll('[data-context]').forEach(b=>b.addEventListener('click',()=>dispatch({type:'context',value:b.dataset.context},false)));
  document.querySelectorAll('[data-category]').forEach(b=>b.addEventListener('change',()=>dispatch({type:'category',value:b.dataset.category},false)));
  $('focus-connections').addEventListener('click',()=>dispatch({type:'scope',value:'connections'},false));
  $('show-all').addEventListener('click',()=>dispatch({type:'scope',value:'all'},false));
  for (const id of ['path-start','path-end']) {
    $(id).addEventListener('change',event=>dispatch({type:id,value:event.target.value || null},false));
  }
  for (const [id, type] of [['use-selected-start','path-start'],['use-selected-end','path-end']]) {
    $(id).addEventListener('click',()=>dispatch({type,value:state.selected},false));
  }
  $('clear-path').addEventListener('click',()=>dispatch({type:'clear-path'},false));
  $('history-back').addEventListener('click',()=>dispatch({type:'back'},false));
  $('history-forward').addEventListener('click',()=>dispatch({type:'forward'},false));
  $('reset').addEventListener('click',()=>dispatch({type:'reset'},false));
  $('start-exploring').addEventListener('click',()=>dispatch({type:'select',value:$('start-exploring').dataset.suggested},true));
  $('zoom-in').addEventListener('click',()=>zoom(1.25));$('zoom-out').addEventListener('click',()=>zoom(.8));$('fit').addEventListener('click',fit);
  $('credits-open').addEventListener('click',()=>$('credits').showModal());
  $('credits-close').addEventListener('click',()=>$('credits').close());
  render();
})();
