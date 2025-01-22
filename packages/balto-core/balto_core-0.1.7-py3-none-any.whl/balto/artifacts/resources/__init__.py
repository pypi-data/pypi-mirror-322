from balto.artifacts.resources.base import BaseResource, Docs, FileHash, GraphResource
from balto.artifacts.resources.v1.analysis import Analysis

# alias to latest resource definitions
from balto.artifacts.resources.v1.components import (
    ColumnInfo,
    CompiledResource,
    Contract,
    DeferRelation,
    DependsOn,
    FreshnessThreshold,
    HasRelationMetadata,
    InjectedCTE,
    NodeVersion,
    ParsedResource,
    ParsedResourceMandatory,
    Quoting,
    RefArgs,
    Time,
)
from balto.artifacts.resources.v1.config import (
    Hook,
    NodeAndTestConfig,
    NodeConfig,
    TestConfig,
)
from balto.artifacts.resources.v1.documentation import Documentation
from balto.artifacts.resources.v1.exposure import (
    Exposure,
    ExposureConfig,
    ExposureType,
    MaturityType,
)
from balto.artifacts.resources.v1.generic_test import GenericTest, TestMetadata
from balto.artifacts.resources.v1.group import Group
from balto.artifacts.resources.v1.hook import HookNode
from balto.artifacts.resources.v1.macro import Macro, MacroArgument, MacroDependsOn
from balto.artifacts.resources.v1.metric import (
    ConstantPropertyInput,
    ConversionTypeParams,
    CumulativeTypeParams,
    Metric,
    MetricConfig,
    MetricInput,
    MetricInputMeasure,
    MetricTimeWindow,
    MetricTypeParams,
)
from balto.artifacts.resources.v1.model import Model, ModelConfig, TimeSpine
from balto.artifacts.resources.v1.owner import Owner
from balto.artifacts.resources.v1.saved_query import (
    Export,
    ExportConfig,
    QueryParams,
    SavedQuery,
    SavedQueryConfig,
    SavedQueryMandatory,
)
from balto.artifacts.resources.v1.schedule import Schedule, ScheduleConfig
from balto.artifacts.resources.v1.seed import Seed, SeedConfig
from balto.artifacts.resources.v1.semantic_layer_components import (
    FileSlice,
    SourceFileMetadata,
    WhereFilter,
    WhereFilterIntersection,
)
from balto.artifacts.resources.v1.semantic_model import (
    Defaults,
    Dimension,
    DimensionTypeParams,
    DimensionValidityParams,
    Entity,
    Measure,
    MeasureAggregationParameters,
    NodeRelation,
    NonAdditiveDimension,
    SemanticModel,
    SemanticModelConfig,
)
from balto.artifacts.resources.v1.singular_test import SingularTest
from balto.artifacts.resources.v1.snapshot import Snapshot, SnapshotConfig
from balto.artifacts.resources.v1.source_definition import (
    ExternalPartition,
    ExternalTable,
    ParsedSourceMandatory,
    SourceConfig,
    SourceDefinition,
)
from balto.artifacts.resources.v1.sql_operation import SqlOperation
from balto.artifacts.resources.v1.unit_test_definition import (
    UnitTestConfig,
    UnitTestDefinition,
    UnitTestFormat,
    UnitTestInputFixture,
    UnitTestNodeVersions,
    UnitTestOutputFixture,
    UnitTestOverrides,
)
