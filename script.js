window.onload = function() {
    fetch('/graph_data')
    .then(response => response.json())
    .then(data => {
        const nodes = new vis.DataSet(data.nodes);
        const edges = new vis.DataSet(data.edges);

        const container = document.getElementById('mynetwork');
        const network = new vis.Network(container, {
            nodes: nodes,
            edges: edges
        }, {});
    });
};