from dataclasses import dataclass
from typing import Optional

from slicebug.config.keys import Keys
from slicebug.config.machine_profile import MachineProfiles, MachineProfile


@dataclass
class Config:
    keys: Optional[Keys]
    profiles: Optional[MachineProfiles]
    profile_name: Optional[str]
    profile: Optional[MachineProfile]

    @classmethod
    def load(cls, config_root, profile_name):
        keys = Keys.load(config_root)
        profiles = MachineProfiles.load(config_root)

        profile_requested = profile_name is not None

        if (
            (profile_name is None)
            and (profiles is not None)
            and (len(profiles.profiles) > 0)
        ):
            # no profile requested, but maybe we can guess one
            if len(profiles.profiles) == 1:
                profile_name = next(iter(profiles.profiles.keys()))
            elif "default" in profiles.profiles:
                profile_name = "default"

        profile = None
        if (
            (profile_name is not None)
            and (profiles is not None)
            and (profile_name in profiles.profiles)
        ):
            profile = profiles.profiles[profile_name]
        elif profile_requested:
            raise ValueError(f"profile {profile_name} does not exist")

        return cls(
            keys=keys,
            profiles=profiles,
            profile_name=profile_name,
            profile=profile,
        )
