# Link Analysis

Implementing three algorithms : HITS, PageRank and SimRank.

## Structure 

```
dataset/
    graph_1.txt
    graph_2.txt
    ...
    
modules/
    hits.py
    page_rank.py
    sim_rank.py

link_analysis.py (main)
```

* python 3.6
* run `python link_analysis dataset/graph_1.txt`

## Implement Detail

* First of all, create graph ... 
    * init sources, targets as defaultdict with list
    * read file per line, record forward, backward edge
    * return an object `Graph(node, sources, targets)`

* for hits module ...
    * init auth, hubs with 1.0
    * update auth by sum hubs
    * update hubs by sum auth
    * until max_iteration or delta < epison

* for page_rank module ...
    * init rank with `1.0 / num_node`, damping factor=0.15
    * update rank by sum `rank[child] / len(child_out)`
    * until max_iteration or delta < epison

* for sim_rank module
    * init S with identity matrix,
    * iter all maxtrix, skip i==j or there is no in-neighbor
    * update maxtrix with average of sum of `S(Ii[a], Ii[b])`
    * until max_iteration or delta < epison

---
* all delta is one-norm normalization
* To increase auth, hubs and PageRank, just add link to node 1

## Result Analysis

* for graph_1 ...
    ```
    // before
    auth: {1: 0.0, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2, 6: 0.2}
    hubs: {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2, 6: 0.0}
    rank: {1: 0.025, 2: 0.0462, 3: 0.0643, 4: 0.0797, 5: 0.0927, 6: 0.1038}
    
    // after
    auth: {1: 0.125, 2: 0.375, 3: 0.125, 4: 0.125, 5: 0.125, 6: 0.125}
    hubs: {1: 0.5,   2: 0.125, 3: 0.125, 4: 0.125, 5: 0.125, 6: 0.0}
    rank: {1: 0.073, 2: 0.0565, 3: 0.073, 4: 0.0879, 5: 0.0997, 6: 0.1115}
    ```
    * before: there is no node link to node_1
    * after: add a link to node_1, so its auth increase (by others hubs)

* for graph_2:
    ```
    // before
    auth: {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2}
    hubs: {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2}
    rank: {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2, 5: 0.2}
    
    // after
    auth: {1: 0.4, 2: 0.3, 3: 0.1, 4: 0.1, 5: 0.1}
    hubs: {1: 0.4, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.3}
    rank: {1: 0.3282, 2: 0.1679, 3: 0.178, 4: 0.1739, 5: 0.1841}
    ```
    * the graph is a circle, so all auth = 0.2 (`1 / num_node`)
    * by add a link (not from node_5) to node_1, node_1's hubs ↑
    * by add a link from node_1 to a no connected node, node_1's auth ↑

* The reason that simply add a link to node_1 can ↑ is because the graph is not fully connected graph 

## Computation Perfromance Analysis

|  | (node, edge) |HITS | PageRank | SimRank |
| -------- | -------- | -------- | -------- | -------- |
| graph_4 | (7, 18) | 0 | 0 | 0.012 |
| graph_5 | (469, 1102) | 0.004 | 0.004 | 15.75 |
| graph_6 | (1228, 5220) | 0.012 | 0.016 | x |
| directed | (231, 43832) | 0.015 | 0.075 | x |
| bi-directed | (231, 87664*) | 0.010 | 0.015 | x |

> 231 nodes should have 53361 edges, so 87664 is the line in txt, not really edge number.
> 

* We can see SimRank is the slowest, because it need iter n * n matrix, while others is iter number of edge 
* Compare graph_5 and graph_6, time is (about) propotional to edge
* Compare directed and bi-directed, we can see page rank is faster in bi-directed than in directed.
* I guess if a graph is fully-connected, it converge soon 

## Discussion

* I learned how to implement link analysis algorithm in detail in this project.
* HITS algorithm is beautiful in theory (use adjust matrix), and also works in real world (converge soon).
* But HITS algorithm is easy to adjust auth, hubs in web, just add link to other, or make other add link to me, so it's not a good solution for search engine.
* Thanks to TAs for prepare dataset. If there is a large dataset, it will be a new grading reference by cost time.

## Question & Discussion

* More limitations about link analysis algorithms:
    * link analysis is link-based algorithm, so we can set some limitation on links
    * such as each node can have 5 out-neighbor at most
    * or give reward / punishment to a SCC(Strongly Connected Component) or else.
* Can link analysis algorithms really find the "important" pages from Web?
    * may be not, since we can easily adjust our auth, hubs by add link
    * for example, we can create many website (even with different domain) to create a group. In group, we link to each other, or the most "important" page
* What are practical issues when implement these algorithms in a real Web?
    * according to [Total number of Websites](http://www.internetlivestats.com/total-number-of-websites/), there is about 2 billion website in the world
    * so the most issue is, how to find "important" page in a few second with large data
    * also, web page is active (creating / deleting), so we need to maitain our table (if used)
* What do the result say for your actor/movie graph?
    * uh..., there is no movie graph in our dataset this year.
* Any new idea about the link analysis algorithm?
    * maybe we can use machine learing to learn the result, such as use link as X, hubs as Y
* What is the effect of “C” parameter in SimRank?
    * C is decay factor
    * because the original formula is recursive, we need a decay factor to converge.
    * if C is small, it converge soon
* Design a new link-based similarity measurement
    * give up
