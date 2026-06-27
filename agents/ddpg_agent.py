"""
DDPG Agent - Deep Deterministic Policy Gradient
Converted from TD3Agent.

Key differences from TD3:
1. Single critic network (no twin critics)
2. No target policy smoothing (no noise added to target actions)
3. No delayed policy updates (actor updates every step)
4. Exploration via Ornstein-Uhlenbeck (OU) noise instead of Gaussian
"""

# This repository is intended as a portfolio demonstration of a cascaded DDPG quadcopter controller. 
# To protect original research and thesis work, this file is not provided.