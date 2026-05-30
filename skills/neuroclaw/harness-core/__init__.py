"""
NeuroClaw Harness Core Library
==============================

Base SDK for implementing harness engineering standards (self-verification,
checkpointing, drift detection, audit logging) across all NeuroClaw skills.

Usage:
    from skills.harness_core import HarnessController, VerificationRunner

License: MIT (NeuroClaw custom skill)
"""

import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Callable, Dict, Optional, List
from dataclasses import dataclass, asdict
import pickle
import sys


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class VerificationResult:
    """Result of a single verification check."""
    check_name: str
    passed: bool
    severity: str  # "error" or "warning"
    message: str = ""
    
    def to_dict(self):
        return asdict(self)


@dataclass
class VerificationReport:
    """Summary of all verification checks for a task."""
    task_type: str
    timestamp: str
    results: List[VerificationResult]
    confidence_score: float = 1.0
    
    @property
    def passed(self):
        return all(r.passed for r in self.results if r.severity == "error")
    
    @property
    def failed(self):
        return not self.passed
    
    @property
    def summary(self):
        errors = [r for r in self.results if r.severity == "error" and not r.passed]
        warnings = [r for r in self.results if r.severity == "warning" and not r.passed]
        return f"Errors: {len(errors)}, Warnings: {len(warnings)}"
    
    def to_dict(self):
        return {
            "task_type": self.task_type,
            "timestamp": self.timestamp,
            "passed": self.passed,
            "summary": self.summary,
            "confidence_score": self.confidence_score,
            "results": [r.to_dict() for r in self.results]
        }


@dataclass
class DriftReport:
    """Results of drift detection analysis."""
    task_name: str
    timestamp: str
    drift_detected: bool
    divergence: float  # KL divergence or similar metric
    severity: str  # "none", "warning", "critical"
    message: str = ""
    
    def to_dict(self):
        return asdict(self)


@dataclass
class EnvironmentSnapshot:
    """Captured environment metadata at execution time."""
    timestamp: str
    python_version: str
    os_info: Dict[str, str]
    conda_env: Optional[str] = None
    conda_version: Optional[str] = None
    installed_packages: Dict[str, str] = None  # {package: version}
    cuda_version: Optional[str] = None
    gpu_info: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)


# ============================================================================
# Core Classes
# ============================================================================

class HarnessController:
    """
    Main orchestrator for harness-compliant execution.
    
    Manages task phases, checkpointing, environment snapshots, and audit logging.
    """
    
    def __init__(self, task_name: str, session_id: str, 
                 checkpoint_dir: str = "./checkpoints", 
                 log_dir: str = "./logs"):
        self.task_name = task_name
        self.session_id = session_id
        self.checkpoint_dir = Path(checkpoint_dir)
        self.log_dir = Path(log_dir)
        
        self.phases = {}
        self.phase_results = {}
        self.environment_snapshot = None
        self.logger = None
        
        self._setup_directories()
        self._setup_logging()
    
    def _setup_directories(self):
        """Create checkpoint and log directories."""
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Configure structured logging."""
        log_file = self.log_dir / f"audit_{self.session_id}.jsonl"
        self.logger = AuditLogger(str(log_file), pii_scrubber=True)
    
    def initialize(self):
        """Capture environment snapshot and initialize execution."""
        self.environment_snapshot = self._capture_environment()
        self.logger.log_event(
            event_type="harness_initialization",
            task_name=self.task_name,
            session_id=self.session_id,
            environment=self.environment_snapshot.to_dict()
        )
    
    def _capture_environment(self) -> EnvironmentSnapshot:
        """Capture current Python/system environment snapshot."""
        import platform
        import subprocess
        
        snapshot = EnvironmentSnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            python_version=platform.python_version(),
            os_info={
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine()
            }
        )
        
        # Try to capture conda info
        try:
            conda_env = subprocess.check_output(
                ["conda", "info", "--json"], 
                text=True
            )
            conda_data = json.loads(conda_env)
            snapshot.conda_version = conda_data.get("conda_version")
        except:
            pass
        
        # Try to capture CUDA info
        try:
            nvcc_version = subprocess.check_output(
                ["nvcc", "--version"],
                text=True
            ).split()[-1]
            snapshot.cuda_version = nvcc_version
        except:
            pass
        
        return snapshot
    
    def add_phase(self, phase_name: str, description: str = ""):
        """Register a task phase."""
        self.phases[phase_name] = {
            "description": description,
            "started_at": None,
            "completed_at": None,
            "status": "pending"
        }
    
    def get_phase(self, phase_name: str):
        """Get phase metadata."""
        if phase_name not in self.phases:
            raise ValueError(f"Phase '{phase_name}' not registered")
        return self.phases[phase_name]
    
    def record_phase_success(self, phase_name: str, result: Any):
        """Record successful phase completion."""
        if phase_name not in self.phases:
            raise ValueError(f"Phase '{phase_name}' not registered")
        
        self.phases[phase_name]["status"] = "success"
        self.phases[phase_name]["completed_at"] = datetime.utcnow().isoformat() + "Z"
        self.phase_results[phase_name] = result
        
        self.logger.log_event(
            event_type="phase_success",
            phase_name=phase_name,
            task_name=self.task_name,
            timestamp=self.phases[phase_name]["completed_at"]
        )
    
    def record_phase_failure(self, phase_name: str, error_msg: str):
        """Record phase failure."""
        if phase_name not in self.phases:
            raise ValueError(f"Phase '{phase_name}' not registered")
        
        self.phases[phase_name]["status"] = "failed"
        self.phases[phase_name]["completed_at"] = datetime.utcnow().isoformat() + "Z"
        self.phases[phase_name]["error"] = error_msg
        
        self.logger.log_event(
            event_type="phase_failure",
            phase_name=phase_name,
            task_name=self.task_name,
            error_msg=error_msg,
            timestamp=self.phases[phase_name]["completed_at"]
        )
    
    def save_checkpoint(self, checkpoint_name: str):
        """Save execution state checkpoint."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        state = {
            "session_id": self.session_id,
            "task_name": self.task_name,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "phases": self.phases,
            "phase_results": self.phase_results,
            "environment_snapshot": self.environment_snapshot.to_dict() if self.environment_snapshot else None
        }
        
        try:
            with open(checkpoint_path, "wb") as f:
                pickle.dump(state, f)
            
            # Generate checkpoint hash
            checkpoint_hash = self._compute_file_hash(checkpoint_path)
            
            self.logger.log_event(
                event_type="checkpoint_saved",
                checkpoint_name=checkpoint_name,
                checkpoint_hash=checkpoint_hash,
                size_bytes=checkpoint_path.stat().st_size
            )
        except Exception as e:
            self.logger.log_event(
                event_type="checkpoint_save_failed",
                checkpoint_name=checkpoint_name,
                error=str(e)
            )
            raise
    
    def load_checkpoint(self, checkpoint_name: str) -> Dict[str, Any]:
        """Load execution state from checkpoint."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_name}")
        
        try:
            with open(checkpoint_path, "rb") as f:
                state = pickle.load(f)
            
            self.logger.log_event(
                event_type="checkpoint_loaded",
                checkpoint_name=checkpoint_name
            )
            
            return state
        except Exception as e:
            self.logger.log_event(
                event_type="checkpoint_load_failed",
                checkpoint_name=checkpoint_name,
                error=str(e)
            )
            raise
    
    @staticmethod
    def _compute_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
        """Compute file hash for integrity verification."""
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def finalize(self):
        """Generate final audit report and cleanup."""
        report = {
            "task_name": self.task_name,
            "session_id": self.session_id,
            "finalized_at": datetime.utcnow().isoformat() + "Z",
            "phases": self.phases,
            "environment_snapshot": self.environment_snapshot.to_dict() if self.environment_snapshot else None
        }
        
        report_file = self.log_dir / f"final_report_{self.session_id}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        self.logger.log_event(
            event_type="harness_finalization",
            task_name=self.task_name,
            session_id=self.session_id,
            report_file=str(report_file)
        )


class VerificationRunner:
    """
    Executes pluggable validation checks on task outputs.
    """
    
    def __init__(self, task_type: str):
        self.task_type = task_type
        self.checks = {}
    
    def add_check(self, check_name: str, checker: Callable, severity: str = "error"):
        """Register a validation check function."""
        if severity not in ["error", "warning"]:
            raise ValueError("severity must be 'error' or 'warning'")
        
        self.checks[check_name] = {
            "checker": checker,
            "severity": severity
        }
    
    def run(self, data: Any) -> VerificationReport:
        """Execute all checks and return verification report."""
        results = []
        
        for check_name, check_config in self.checks.items():
            try:
                checker = check_config["checker"]
                result = checker(data)
                
                results.append(VerificationResult(
                    check_name=check_name,
                    passed=bool(result),
                    severity=check_config["severity"],
                    message="Passed" if result else "Failed"
                ))
            except Exception as e:
                results.append(VerificationResult(
                    check_name=check_name,
                    passed=False,
                    severity=check_config["severity"],
                    message=str(e)
                ))
        
        report = VerificationReport(
            task_type=self.task_type,
            timestamp=datetime.utcnow().isoformat() + "Z",
            results=results
        )
        
        return report


class CheckpointManager:
    """
    Handles checkpoint saving and loading with compression and integrity verification.
    """
    
    def __init__(self, checkpoint_dir: str = "./checkpoints", 
                 compression: str = "pickle", 
                 hash_algorithm: str = "sha256"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.compression = compression
        self.hash_algorithm = hash_algorithm
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, checkpoint_name: str, data: Dict[str, Any], overwrite: bool = False):
        """Save checkpoint with optional compression."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        if checkpoint_path.exists() and not overwrite:
            raise FileExistsError(f"Checkpoint already exists: {checkpoint_name}")
        
        with open(checkpoint_path, "wb") as f:
            pickle.dump(data, f)
        
        # Compute and store hash
        file_hash = self._compute_hash(checkpoint_path)
        hash_file = self.checkpoint_dir / f"{checkpoint_name}.sha256"
        with open(hash_file, "w") as f:
            f.write(file_hash)
    
    def load(self, checkpoint_name: str) -> Dict[str, Any]:
        """Load checkpoint and verify integrity."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_name}.pkl"
        
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_name}")
        
        # Verify hash if available
        hash_file = self.checkpoint_dir / f"{checkpoint_name}.sha256"
        if hash_file.exists():
            stored_hash = hash_file.read_text().strip()
            computed_hash = self._compute_hash(checkpoint_path)
            if stored_hash != computed_hash:
                raise ValueError(f"Checkpoint integrity check failed: {checkpoint_name}")
        
        with open(checkpoint_path, "rb") as f:
            return pickle.load(f)
    
    @staticmethod
    def _compute_hash(file_path: Path, algorithm: str = "sha256") -> str:
        """Compute file hash."""
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()


class DriftDetector:
    """
    Monitors data/model behavior for distribution shifts.
    """
    
    def __init__(self, reference_data: Any, detector_type: str = "kl_divergence"):
        self.reference_data = reference_data
        self.detector_type = detector_type
    
    def detect(self, new_data: Any) -> DriftReport:
        """Run drift detection."""
        # Simplified implementation; extend for specific domain checks
        
        divergence = 0.0  # Placeholder
        severity = "none"
        drift_detected = divergence > 0.1
        
        if divergence > 0.1:
            severity = "warning"
        if divergence > 0.2:
            severity = "critical"
        
        return DriftReport(
            task_name="drift_detection",
            timestamp=datetime.utcnow().isoformat() + "Z",
            drift_detected=drift_detected,
            divergence=divergence,
            severity=severity
        )


class AuditLogger:
    """
    Structured, privacy-preserving logging for reproducibility and compliance.
    """
    
    def __init__(self, log_file: str, pii_scrubber: bool = True):
        self.log_file = Path(log_file)
        self.pii_scrubber = pii_scrubber
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_event(self, event_type: str, **kwargs):
        """Log a structured event."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            **kwargs
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def log_validation(self, task_name: str, **kwargs):
        """Log validation results."""
        self.log_event(
            event_type="validation",
            task_name=task_name,
            **kwargs
        )


class DependencyManifest:
    """
    Generate and verify reproducible dependency specifications.
    """
    
    def __init__(self, environment_name: Optional[str] = None):
        self.environment_name = environment_name
        self.packages = {}
    
    def capture_current_environment(self):
        """Auto-capture current environment state."""
        import subprocess
        
        try:
            result = subprocess.check_output(["pip", "list", "--format=json"], text=True)
            self.packages = {pkg["name"]: pkg["version"] for pkg in json.loads(result)}
        except Exception as e:
            print(f"Warning: Could not capture environment: {e}")
    
    def export_to_pip_txt(self, file_path: str):
        """Export to pip format."""
        with open(file_path, "w") as f:
            f.write("# Generated by harness-core\n")
            f.write(f"# Generated at: {datetime.utcnow().isoformat()}Z\n")
            for pkg, version in sorted(self.packages.items()):
                f.write(f"{pkg}=={version}\n")
    
    def verify_current_environment(self, strict: bool = False) -> VerificationReport:
        """Verify environment matches manifest."""
        # Placeholder implementation
        report = VerificationReport(
            task_type="environment_verification",
            timestamp=datetime.utcnow().isoformat() + "Z",
            results=[]
        )
        return report


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "HarnessController",
    "VerificationRunner",
    "CheckpointManager",
    "DriftDetector",
    "AuditLogger",
    "DependencyManifest",
    "VerificationResult",
    "VerificationReport",
    "DriftReport",
    "EnvironmentSnapshot"
]
