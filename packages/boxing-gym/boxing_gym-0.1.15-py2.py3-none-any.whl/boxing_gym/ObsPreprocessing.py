import cv2
import numpy as np
import gymnasium as gym
from gymnasium.core import WrapperActType, WrapperObsType
from gymnasium.spaces import Box
from typing import Any, SupportsFloat


class ObsPreprocessing(gym.Wrapper, gym.utils.RecordConstructorArgs):
    """Preprocessing for Punch Out environment.

    Includes preprocessing steps such as:
    - Frame skipping
    - Grayscale conversion
    - Resizing frames
    """

    def __init__(
        self,
        env: gym.Env,
        frame_skip: int = 4,
        screen_size: int = 84,
        grayscale_obs: bool = True,
        grayscale_newaxis: bool = False,
        scale_obs: bool = False,
    ):
        """Initialize MarioPreprocessing wrapper.

        Args:
            env (gym.Env): The base environment to wrap.
            frame_skip (int): The number of frames to skip between observations.
            screen_size (int): The size to which frames are resized.
            grayscale_obs (bool): Whether to convert frames to grayscale.
            grayscale_newaxis (bool): Add a channel axis to grayscale frames.
            scale_obs (bool): Normalize observation values to [0, 1].
        """
        gym.utils.RecordConstructorArgs.__init__(
            self,
            frame_skip=frame_skip,
            screen_size=screen_size,
            grayscale_obs=grayscale_obs,
            grayscale_newaxis=grayscale_newaxis,
            scale_obs=scale_obs,
        )
        gym.Wrapper.__init__(self, env)

        self.frame_skip = frame_skip
        self.screen_size = screen_size
        self.grayscale_obs = grayscale_obs
        self.grayscale_newaxis = grayscale_newaxis
        self.scale_obs = scale_obs

        if self.grayscale_obs:
            # Buffer for grayscale frames
            self.obs_buffer = [
                np.empty(self.env.observation_space.shape[:2], dtype=np.uint8),
                np.empty(self.env.observation_space.shape[:2], dtype=np.uint8),
            ]
        else:
            # Buffer for RGB frames
            self.obs_buffer = [
                np.empty(self.env.observation_space.shape, dtype=np.uint8),
                np.empty(self.env.observation_space.shape, dtype=np.uint8),
            ]

        # Reshaped observation space
        _low, _high, _obs_dtype = (0, 255, np.uint8) if not scale_obs else (0, 1, np.float32)
        _shape = (screen_size, screen_size, 1 if grayscale_obs else 3)
        if grayscale_obs and not grayscale_newaxis:
            _shape = _shape[:-1]  # Remove channel axis
            
        self.observation_space = Box(low=_low, high=_high, shape=_shape, dtype=_obs_dtype)

    def step(
        self, action: WrapperActType
    ) -> tuple[WrapperObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        """Step the environment with preprocessing."""
        total_reward = 0.0
        terminated = False
        truncated = False
        info = {}
        last_obs = None  # Track the last valid observation

        for t in range(self.frame_skip):
            obs, reward, terminated, truncated, info = self.env.step(action)
            total_reward += reward
            last_obs = obs  # Save the last valid observation

            if terminated or truncated:
                break

            if t == self.frame_skip - 2:
                self.obs_buffer[1] = obs
            elif t == self.frame_skip - 1:
                self.obs_buffer[0] = obs
        
        # Ensure the observation buffer is updated even if terminated early
        if terminated or truncated:
            if self.frame_skip > 1:
                self.obs_buffer[1] = last_obs  # Fill missing frames with the last valid observation
                self.obs_buffer[0] = last_obs

        return self._get_obs(), total_reward, terminated, truncated, info

    def reset(self, **kwargs) -> tuple[WrapperObsType, dict[str, Any]]:
        """Reset the environment with preprocessing."""
        obs, info = self.env.reset(**kwargs)

        if self.grayscale_obs:
            obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
        self.obs_buffer[0].fill(0)  # Clear the second frame buffer
        self.obs_buffer[1] = obs

        return self._get_obs(), info

    def _get_obs(self):
        if self.frame_skip > 1:  # Max-pooling for skipped frames
            np.maximum(self.obs_buffer[0], self.obs_buffer[1], out=self.obs_buffer[0])

        # Convert RGB to grayscale if enabled
        if self.grayscale_obs and self.obs_buffer[0].ndim == 3:
            self.obs_buffer[0] = cv2.cvtColor(self.obs_buffer[0], cv2.COLOR_RGB2GRAY)

        # **Center Crop to 84x84 region**
        original_height, original_width = self.obs_buffer[0].shape[:2]
        crop_height, crop_width = 168, 168  # Desired crop size

        # Calculate cropping coordinates
        top = (original_height - crop_height) // 2
        left = (original_width - crop_width) // 2
        bottom = top + crop_height
        right = left + crop_width

        # Crop the center of the observation
        cropped_obs = self.obs_buffer[0][top:bottom, left:right]
        
        # Resize the cropped observation
        obs = cv2.resize(
            cropped_obs,
            (self.screen_size, self.screen_size),
            interpolation=cv2.INTER_AREA,
        )

        # Scale the observation if needed
        if self.scale_obs:
            obs = np.asarray(obs, dtype=np.float32) / 255.0
        else:
            obs = np.asarray(obs, dtype=np.uint8)

        # Add a channel axis for grayscale if needed
        if self.grayscale_obs and self.grayscale_newaxis:
            obs = np.expand_dims(obs, axis=-1)

        # self.save_observation(obs)

        return obs
    
    def save_observation(self, observation, filename="observation.png"):
        """Save the preprocessed observation as a BMP or PNG file.

        Args:
            observation: The preprocessed observation to save.
            filename: The filename of the image file.
        """
        # Check if the observation has an extra channel axis for grayscale
        if observation.ndim == 3 and observation.shape[-1] == 1:
            observation = observation.squeeze(-1)  # Remove the channel axis

        # Save the image
        success = cv2.imwrite(filename, observation)
        if not success:
            raise IOError(f"Failed to save the observation to {filename}")
        print(f"Saved observation to {filename}")
