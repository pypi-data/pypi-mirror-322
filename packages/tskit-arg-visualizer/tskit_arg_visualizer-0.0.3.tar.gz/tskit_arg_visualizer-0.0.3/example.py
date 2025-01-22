import msprime
import random
import tskit_arg_visualizer

# Generate a random tree sequence with record_full_arg=True so that you get marked recombination nodes
ts_rs = random.randint(0,10000) 
print(ts_rs)  
ts = msprime.sim_ancestry(
    samples=10,
    recombination_rate=1e-8,
    sequence_length=3_000,
    population_size=10_000,
    record_full_arg=True,
    random_seed=8680
)

d3arg = tskit_arg_visualizer.D3ARG.from_ts(ts=ts, progress=True)

#d3arg.draw()
#d3arg.draw_node(node=20)
d3arg.draw_nodes(node=[20, 42], degree=2)