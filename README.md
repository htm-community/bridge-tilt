# Bridge Tilt Experiment

The data in `data/raw` was provided by John Blackburn from the NuPIC mailing lists. His problem is to find anomalies in the bridge tilt data, which could be affected by temperature readings.

This experiment is a work in progress.

- [X] Convert raw data into NuPIC input files
- [X] Produce swarm configuration for an input file
- [X] Create swarm script to run a swarm over input
- [X] Evaluate model params output by swarm
- [X] Run NuPIC with model params output by swarm
- [X] Evaluate NuPIC output
- [ ] Experiment with different model params based on swarm output
- [ ] Train an anomaly model on first two years data, serialize model
- [ ] Resurrect trained model and run third year with plot
- [ ] Try an anomaly model with manually encoded temperature as a factor
- [ ] Experiment with using multiple models simultaneously
