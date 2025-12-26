"""
Advanced Monitoring & Observability Stack
Comprehensive logging, metrics, tracing, and alerting
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import json
from enum import Enum
from dataclasses import dataclass, asdict
import time
from functools import wraps


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(Enum):
    """Metric types"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: str
    message: str
    service: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    user_id: Optional[int] = None
    entity_id: Optional[int] = None
    metadata: Dict[str, Any] = None
    
    def to_json(self) -> str:
        """Convert to JSON for structured logging"""
        return json.dumps(asdict(self), default=str)


@dataclass
class Metric:
    """Metric data point"""
    name: str
    value: float
    type: MetricType
    timestamp: datetime
    tags: Dict[str, str] = None
    
    def to_datadog_format(self) -> Dict[str, Any]:
        """Convert to Datadog metric format"""
        return {
            "metric": self.name,
            "points": [[self.timestamp.timestamp(), self.value]],
            "type": self.type.value,
            "tags": [f"{k}:{v}" for k, v in (self.tags or {}).items()]
        }
    
    def to_prometheus_format(self) -> str:
        """Convert to Prometheus metric format"""
        tags_str = ",".join([f'{k}="{v}"' for k, v in (self.tags or {}).items()])
        return f"{self.name}{{{tags_str}}} {self.value} {int(self.timestamp.timestamp() * 1000)}"


class StructuredLogger:
    """Structured logging with context"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup JSON structured logging"""
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def _create_log_entry(
        self,
        level: LogLevel,
        message: str,
        trace_id: Optional[str] = None,
        user_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        **metadata
    ) -> LogEntry:
        """Create structured log entry"""
        return LogEntry(
            timestamp=datetime.utcnow().isoformat(),
            level=level.value,
            message=message,
            service=self.service_name,
            trace_id=trace_id,
            user_id=user_id,
            entity_id=entity_id,
            metadata=metadata
        )
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        entry = self._create_log_entry(LogLevel.DEBUG, message, **kwargs)
        self.logger.debug(entry.to_json())
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        entry = self._create_log_entry(LogLevel.INFO, message, **kwargs)
        self.logger.info(entry.to_json())
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        entry = self._create_log_entry(LogLevel.WARNING, message, **kwargs)
        self.logger.warning(entry.to_json())
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        entry = self._create_log_entry(LogLevel.ERROR, message, **kwargs)
        self.logger.error(entry.to_json())
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        entry = self._create_log_entry(LogLevel.CRITICAL, message, **kwargs)
        self.logger.critical(entry.to_json())


class MetricsCollector:
    """Collect and export metrics to monitoring systems"""
    
    def __init__(self):
        self.metrics: List[Metric] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
    
    def increment_counter(
        self,
        name: str,
        value: float = 1.0,
        tags: Dict[str, str] = None
    ):
        """Increment a counter metric"""
        if name not in self.counters:
            self.counters[name] = 0.0
        
        self.counters[name] += value
        
        metric = Metric(
            name=name,
            value=self.counters[name],
            type=MetricType.COUNTER,
            timestamp=datetime.utcnow(),
            tags=tags
        )
        self.metrics.append(metric)
    
    def set_gauge(
        self,
        name: str,
        value: float,
        tags: Dict[str, str] = None
    ):
        """Set a gauge metric"""
        self.gauges[name] = value
        
        metric = Metric(
            name=name,
            value=value,
            type=MetricType.GAUGE,
            timestamp=datetime.utcnow(),
            tags=tags
        )
        self.metrics.append(metric)
    
    def record_histogram(
        self,
        name: str,
        value: float,
        tags: Dict[str, str] = None
    ):
        """Record a histogram metric"""
        metric = Metric(
            name=name,
            value=value,
            type=MetricType.HISTOGRAM,
            timestamp=datetime.utcnow(),
            tags=tags
        )
        self.metrics.append(metric)
    
    def get_metrics(self, format: str = "datadog") -> List[Dict[str, Any]]:
        """Get metrics in specified format"""
        if format == "datadog":
            return [m.to_datadog_format() for m in self.metrics]
        elif format == "prometheus":
            return [m.to_prometheus_format() for m in self.metrics]
        else:
            return [asdict(m) for m in self.metrics]
    
    def clear_metrics(self):
        """Clear stored metrics"""
        self.metrics = []


class DistributedTracing:
    """Distributed tracing for request flows"""
    
    def __init__(self):
        self.active_traces: Dict[str, Dict[str, Any]] = {}
    
    def start_trace(
        self,
        trace_id: str,
        operation_name: str,
        tags: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Start a new trace"""
        trace = {
            "trace_id": trace_id,
            "operation_name": operation_name,
            "start_time": datetime.utcnow(),
            "spans": [],
            "tags": tags or {}
        }
        
        self.active_traces[trace_id] = trace
        return trace
    
    def start_span(
        self,
        trace_id: str,
        span_name: str,
        parent_span_id: Optional[str] = None,
        tags: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Start a new span within a trace"""
        import uuid
        
        span_id = str(uuid.uuid4())
        
        span = {
            "span_id": span_id,
            "span_name": span_name,
            "parent_span_id": parent_span_id,
            "start_time": datetime.utcnow(),
            "end_time": None,
            "duration_ms": None,
            "tags": tags or {},
            "logs": []
        }
        
        if trace_id in self.active_traces:
            self.active_traces[trace_id]["spans"].append(span)
        
        return span
    
    def end_span(self, trace_id: str, span_id: str):
        """End a span"""
        if trace_id not in self.active_traces:
            return
        
        trace = self.active_traces[trace_id]
        for span in trace["spans"]:
            if span["span_id"] == span_id:
                span["end_time"] = datetime.utcnow()
                span["duration_ms"] = (
                    span["end_time"] - span["start_time"]
                ).total_seconds() * 1000
                break
    
    def add_span_log(
        self,
        trace_id: str,
        span_id: str,
        message: str,
        fields: Dict[str, Any] = None
    ):
        """Add log to a span"""
        if trace_id not in self.active_traces:
            return
        
        trace = self.active_traces[trace_id]
        for span in trace["spans"]:
            if span["span_id"] == span_id:
                span["logs"].append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "message": message,
                    "fields": fields or {}
                })
                break
    
    def end_trace(self, trace_id: str) -> Dict[str, Any]:
        """End a trace and return trace data"""
        if trace_id not in self.active_traces:
            return None
        
        trace = self.active_traces[trace_id]
        trace["end_time"] = datetime.utcnow()
        trace["duration_ms"] = (
            trace["end_time"] - trace["start_time"]
        ).total_seconds() * 1000
        
        del self.active_traces[trace_id]
        return trace


class PerformanceMonitor:
    """Monitor application performance"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
    
    def monitor_function(self, operation_name: str):
        """Decorator to monitor function performance"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    self.metrics.increment_counter(
                        f"{operation_name}.success",
                        tags={"function": func.__name__}
                    )
                    return result
                except Exception as e:
                    self.metrics.increment_counter(
                        f"{operation_name}.error",
                        tags={"function": func.__name__, "error": str(e)}
                    )
                    raise
                finally:
                    duration = (time.time() - start_time) * 1000
                    self.metrics.record_histogram(
                        f"{operation_name}.duration_ms",
                        duration,
                        tags={"function": func.__name__}
                    )
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    self.metrics.increment_counter(
                        f"{operation_name}.success",
                        tags={"function": func.__name__}
                    )
                    return result
                except Exception as e:
                    self.metrics.increment_counter(
                        f"{operation_name}.error",
                        tags={"function": func.__name__, "error": str(e)}
                    )
                    raise
                finally:
                    duration = (time.time() - start_time) * 1000
                    self.metrics.record_histogram(
                        f"{operation_name}.duration_ms",
                        duration,
                        tags={"function": func.__name__}
                    )
            
            # Return appropriate wrapper based on function type
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator


class AlertManager:
    """Manage alerts based on metrics and thresholds"""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.alert_rules: List[Dict[str, Any]] = []
    
    def add_alert_rule(
        self,
        name: str,
        metric_name: str,
        threshold: float,
        condition: str,  # "greater_than", "less_than", "equals"
        severity: str = "warning"
    ):
        """Add an alert rule"""
        self.alert_rules.append({
            "name": name,
            "metric_name": metric_name,
            "threshold": threshold,
            "condition": condition,
            "severity": severity
        })
    
    def check_metrics(self, metrics: List[Metric]) -> List[Dict[str, Any]]:
        """Check metrics against alert rules"""
        alerts = []
        
        for metric in metrics:
            for rule in self.alert_rules:
                if metric.name == rule["metric_name"]:
                    should_alert = False
                    
                    if rule["condition"] == "greater_than" and metric.value > rule["threshold"]:
                        should_alert = True
                    elif rule["condition"] == "less_than" and metric.value < rule["threshold"]:
                        should_alert = True
                    elif rule["condition"] == "equals" and metric.value == rule["threshold"]:
                        should_alert = True
                    
                    if should_alert:
                        alert = {
                            "rule_name": rule["name"],
                            "metric_name": metric.name,
                            "current_value": metric.value,
                            "threshold": rule["threshold"],
                            "severity": rule["severity"],
                            "timestamp": metric.timestamp.isoformat()
                        }
                        alerts.append(alert)
                        
                        # Log alert
                        self.logger.warning(
                            f"Alert triggered: {rule['name']}",
                            alert_data=alert
                        )
        
        return alerts


# Global monitoring instances
logger = StructuredLogger("reputation-ai")
metrics = MetricsCollector()
tracing = DistributedTracing()
performance_monitor = PerformanceMonitor(metrics)
alert_manager = AlertManager(logger)

# Setup default alert rules
alert_manager.add_alert_rule(
    name="High API Latency",
    metric_name="api.request.duration_ms",
    threshold=100.0,
    condition="greater_than",
    severity="warning"
)

alert_manager.add_alert_rule(
    name="High Error Rate",
    metric_name="api.request.error",
    threshold=10.0,
    condition="greater_than",
    severity="critical"
)

alert_manager.add_alert_rule(
    name="Low Uptime",
    metric_name="system.uptime_percentage",
    threshold=99.99,
    condition="less_than",
    severity="critical"
)
