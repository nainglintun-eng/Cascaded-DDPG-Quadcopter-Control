"""
Cascaded DDPG Config  –  FIXED VERSION
======================================
Fixes applied:
  - AttitudeControllerConfig.MAX_TORQUE = SystemConfig.MAX_TORQUE (was wrong value 5.0)
  - PositionControllerConfig: max_action = 1.0 (normalised), reward rewritten
  - Curriculum: starts with hover phase before helix
"""

# This repository is intended as a portfolio demonstration of a cascaded DDPG quadcopter controller.
# To protect original research and thesis work, this file is not fully provided. Some values have been removed or replaced with placeholders to prevent replication of original research.

import numpy as np


class SystemConfig:
    MASS    = 
    GRAVITY = 
    DT      = 

    IXX = 0.3; IYY = 0.4; IZZ = 0.5
    L   = 0.2

    MAX_THRUST     = 2.0 * MASS * GRAVITY
    MIN_THRUST     = 0.1 * MASS * GRAVITY
    MAX_TORQUE     = (MAX_THRUST / 4.0) * L * 2    # 1.962 Nm
    MAX_TORQUE_YAW = 0.7 * MAX_TORQUE              # 1.373 Nm

    BASE_MISSION_TIME = 50.0
    MAX_STEPS         = int(BASE_MISSION_TIME / DT)

    MAX_POSITION     = 
    MIN_ALTITUDE     = 
    MAX_ALTITUDE     = 
    CRASH_ANGLE      = np.deg2rad(95)
    MAX_VELOCITY     = 
    MAX_ANGULAR_RATE = np.deg2rad(600)

    WIND_TRAINING  = False
    RANDOM_START   = True
    RANDOM_SEED    = 
    WIND_GUST_PROB = 0.0
    WIND_GUST_MAG  = 0.0
    ATTITUDE_MAX_STEPS = 

    A = 9.81; B = 0.01; OMEGA = 0.2; VZ = 1.0


class AttitudeControllerConfig:
    STATE_DIM  = 9
    ACTION_DIM = 3

    ACTOR_LR  = 
    CRITIC_LR = 
    GAMMA = ; TAU = 
    OU_THETA = ; OU_SIGMA =    # Ornstein-Uhlenbeck noise params
    HIDDEN_DIMS = 128
    BATCH_SIZE = 256; BUFFER_SIZE = 200_000; WARMUP_STEPS = 500
    EXPLORATION_NOISE = 0.3; NOISE_DECAY = 0.9998; MIN_NOISE = 0.05

    # FIX: use correct physical torque limit
    MAX_TORQUE = SystemConfig.MAX_TORQUE   # was 5.0, now 1.962 Nm

    EPISODES_PER_PHASE = 
    SUCCESS_THRESHOLD  = np.deg2rad(5.0)
    CONSECUTIVE_SUCCESSES = 
    MAX_EXPECTED_ERROR = np.deg2rad(90.0)
    MAX_EXPECTED_RATE  = 


class PositionControllerConfig:
    STATE_DIM  = 18
    ACTION_DIM = 3

    ACTOR_LR  = 
    CRITIC_LR = 
    GAMMA = ; TAU = 
    OU_THETA = ; OU_SIGMA =    # Ornstein-Uhlenbeck noise params
    HIDDEN_DIMS = 
    BATCH_SIZE = 256; BUFFER_SIZE = 300_000; WARMUP_STEPS = 2_000
    EXPLORATION_NOISE = ; NOISE_DECAY = 0.9998; MIN_NOISE = 

    # FIX: normalised action (body accelerations still, but actor outputs [-1,+1])
    MAX_BODY_ACCELERATION = 15.0   # physical limit
    ACTION_SCALE          = 1.0    # actor max_action

    MIN_THRUST     = SystemConfig.MIN_THRUST
    MAX_THRUST     = SystemConfig.MAX_THRUST
    MAX_TILT_ANGLE = np.deg2rad(45)

    ATTITUDE_PENALTY   = 
    ACTION_PENALTY     = 
    SMOOTHNESS_PENALTY = 
    PRECISION_BONUS    =   # FIX: removed – caused lazy-agent exploit

    REWARD_CONFIG = {
        # To Prevent Original Research
    }

    CURRICULUM_PHASES = [
        # To Prevent Original Research
    ]


class FineTuningConfig:
    EPISODES = 500
    ATTITUDE_LR_SCALE = 0.1
    POSITION_LR_SCALE = 0.3
    NOISE_SCALE = 0.3
    SUCCESS_ERROR = 0.6
    SUCCESS_RATE  = 0.80


class TrainingConfig:
    TRAIN_ATTITUDE_FIRST  = False
    TRAIN_POSITION_SECOND = True
    FINE_TUNE_TOGETHER    = False
    SAVE_FREQUENCY  = 500
    KEEP_BEST_ONLY  = True
    LOG_FREQUENCY   = 5
    EVAL_EPISODES   = 5
    EVAL_FREQUENCY  = 100
    EARLY_STOPPING_PATIENCE  = 50
    MIN_EPISODES_BEFORE_STOP = 100
    NUM_WORKERS = 1


def get_trajectory_function():
    cfg = SystemConfig()

    def trajectory(t, scale=1.0):
        exp_term = np.exp(-cfg.B * t)
        radius   = cfg.A * (1 - exp_term) * scale
        omega_t  = cfg.OMEGA * t
        x = radius * np.cos(omega_t)
        y = radius * np.sin(omega_t)
        z = cfg.VZ * t * scale
        dR = cfg.A * cfg.B * exp_term * scale
        vx = dR*np.cos(omega_t) - radius*cfg.OMEGA*np.sin(omega_t)
        vy = dR*np.sin(omega_t) + radius*cfg.OMEGA*np.cos(omega_t)
        vz = cfg.VZ * scale
        d2R = -cfg.A * cfg.B**2 * exp_term * scale
        ax = d2R*np.cos(omega_t) - 2*dR*cfg.OMEGA*np.sin(omega_t) - radius*cfg.OMEGA**2*np.cos(omega_t)
        ay = d2R*np.sin(omega_t) + 2*dR*cfg.OMEGA*np.cos(omega_t) - radius*cfg.OMEGA**2*np.sin(omega_t)
        az = 0.0
        return np.array([x,y,z]), np.array([vx,vy,vz]), np.array([ax,ay,az])

    return trajectory
