"""Provide JobCaching class that implements caching for jobs"""
from __future__ import annotations

from pathlib import Path

import rtoml
from simpleconf import Config

from .defaults import ProcInputType, ProcOutputType
from .pluginmgr import plugin


class JobCaching:
    """Provide caching functionality of jobs"""

    @property
    def signature_file(self) -> Path:
        """Get the path to the signature file

        Returns:
            The path to the signature file
        """
        return self.metadir / "job.signature.toml"

    async def cache(self) -> None:
        """write signature to signature file"""
        dirsig = (
            self.proc.pipeline.config.dirsig
            if self.proc.dirsig is None
            else self.proc.dirsig
        )
        # Check if mtimes of input is greater than those of output
        try:
            max_mtime = self.script_file.stat().st_mtime
        except FileNotFoundError:
            max_mtime = 0

        for inkey, intype in self.proc.input.type.items():
            if intype == ProcInputType.VAR:
                continue

            if (
                intype in (ProcInputType.FILE, ProcInputType.DIR)
                and self.input[inkey] is not None
            ):
                max_mtime = max(
                    max_mtime, plugin.hooks.get_mtime(self, self.input[inkey], dirsig)
                )

            if (
                intype in (ProcInputType.FILES, ProcInputType.DIRS)
                and self.input[inkey] is not None
            ):
                for file in self.input[inkey]:
                    max_mtime = max(
                        max_mtime,
                        plugin.hooks.get_mtime(self, file, dirsig),
                    )

        for outkey, outval in self._output_types.items():
            if outval in (ProcOutputType.FILE, ProcInputType.DIR):
                max_mtime = max(
                    max_mtime,
                    plugin.hooks.get_mtime(self, self.output[outkey], dirsig),
                )

        signature = {
            "input": {
                "type": self.proc.input.type,
                "data": self.input,
            },
            "output": {"type": self._output_types, "data": self.output},
            "ctime": float("inf") if max_mtime == 0 else max_mtime,
        }
        rtoml.dump(signature, self.signature_file)

    async def _clear_output(self) -> None:
        """Clear output if not cached"""
        self.log("debug", "Clearing previous output files.")
        for outkey, outval in self._output_types.items():
            if outval not in (ProcOutputType.FILE, ProcOutputType.DIR):
                continue

            await plugin.hooks.clear_path(
                self,
                self.output[outkey],
                outval == ProcOutputType.DIR,
            )

    async def _check_cached(self) -> bool:
        """Check if the job is cached based on signature

        Returns:
            True if the job is cached otherwise False
        """
        signature = Config.load(self.signature_file)
        dirsig = (
            self.proc.pipeline.config.dirsig
            if self.proc.dirsig is None
            else self.proc.dirsig
        )

        try:
            # check if inputs/outputs are still the same
            if (
                signature.input.type != self.proc.input.type
                or signature.input.data != self.input
                or signature.output.type != self._output_types
                or signature.output.data != self.output
            ):
                self.log("debug", "Not cached (input or output is different)")
                return False

            # check if any script file is newer
            if self.script_file.stat().st_mtime > signature.ctime + 1e-3:
                self.log(
                    "debug",
                    "Not cached (script file is newer: %s > %s)",
                    self.script_file.stat().st_mtime,
                    signature.ctime,
                )
                return False

            for inkey, intype in self.proc.input.type.items():

                if intype == ProcInputType.VAR or self.input[inkey] is None:
                    continue  # pragma: no cover, covered, a bug of pytest-cov

                if intype in (ProcInputType.FILE, ProcInputType.DIR):
                    if (
                        plugin.hooks.get_mtime(self, self.input[inkey], dirsig)
                        > signature.ctime + 1e-3
                    ):
                        self.log(
                            "debug",
                            "Not cached (Input file is newer: %s)",
                            inkey,
                        )
                        return False

                if intype in (ProcInputType.FILES, ProcInputType.DIRS):
                    for file in self.input[inkey]:
                        if (
                            plugin.hooks.get_mtime(self, file, dirsig)
                            > signature.ctime + 1e-3
                        ):
                            self.log(
                                "debug",
                                "Not cached (One of the input files "
                                "is newer: %s)",
                                inkey,
                            )
                            return False

            for outkey, outval in self._output_types.items():
                if outval not in (ProcOutputType.FILE, ProcOutputType.DIR):
                    continue

                output_exists = await plugin.hooks.output_exists(
                    self,
                    self.output[outkey],
                    outval == ProcOutputType.DIR,
                )
                if not output_exists:
                    self.log(
                        "debug",
                        "Not cached (Output file removed: %s)",
                        outkey,
                    )
                    return False

        except (AttributeError, FileNotFoundError):  # pragma: no cover
            # meaning signature is incomplete
            # or any file is deleted
            return False
        return True

    @property
    async def cached(self) -> bool:
        """Check if a job is cached

        Returns:
            True if the job is cached otherwise False
        """
        out = True
        proc_cache = (
            self.proc.pipeline.config.cache
            if self.proc.cache is None
            else self.proc.cache
        )
        if not proc_cache:
            self.log(
                "debug",
                "Not cached (proc.cache is False)",
            )
            out = False
        elif await self.rc != 0:
            self.log(
                "debug",
                "Not cached (job.rc != 0)",
            )
            out = False
        elif proc_cache == "force":
            try:
                await self.cache()
            except FileNotFoundError:  # pragma: no cover
                out = False
            else:
                out = True
        elif not self.signature_file.is_file():
            self.log(
                "debug",
                "Not cached (signature file not found)",
            )
            out = False
        else:
            out = await self._check_cached()

        if not out:
            await self._clear_output()

        return out
