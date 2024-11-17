from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from collections import defaultdict

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pipeline(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

def is_dag(nodes: List[Dict], edges: List[Dict]) -> bool:
    # Create adjacency list
    graph = defaultdict(list)
    for edge in edges:
        graph[edge['source']].append(edge['target'])
    
    # Track visited nodes
    visited = set()
    temp = set()
    
    def has_cycle(node):
        if node in temp:
            return True
        if node in visited:
            return False
            
        temp.add(node)
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
        temp.remove(node)
        visited.add(node)
        return False
    
    # Check each node for cycles
    node_ids = [node['id'] for node in nodes]
    for node_id in node_ids:
        if node_id not in visited:
            if has_cycle(node_id):
                return False
    return True

@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    is_dag_result = is_dag(pipeline.nodes, pipeline.edges)
    
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag_result,
        "Name": "AKib"
    }