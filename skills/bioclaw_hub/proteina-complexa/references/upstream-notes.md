# Proteina-Complexa Upstream Notes

This skill is based on the public NVIDIA Digital Bio `proteina` repository.

What is most important for BioClaw routing:

- Proteina is a flow-based protein backbone generator rather than a sequence-design model.
- The publicly described strengths are fold-conditioned generation, long-chain generation, and large-scale backbone sampling.
- The upstream setup requires additional data and weight bundles referenced from the project README.
- Commercial-use and redistribution questions should be checked against the upstream NVIDIA license before deployment.

Recommended BioClaw framing:

- Route to this skill when the user wants controllable backbone generation.
- Route to `proteinmpnn` or `solublempnn` immediately after backbone generation.
- Route to `chai1-structure-prediction`, `boltz-structure-prediction`, or `alphafold2-multimer` for validation.
- Route to `protein-design-qc` for final filtering and ranking.
