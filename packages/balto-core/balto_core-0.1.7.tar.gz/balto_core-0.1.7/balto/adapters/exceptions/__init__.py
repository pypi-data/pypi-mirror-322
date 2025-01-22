from balto.adapters.exceptions.alias import AliasError, DuplicateAliasError
from balto.adapters.exceptions.cache import (
    CacheInconsistencyError,
    DependentLinkNotCachedError,
    NewNameAlreadyInCacheError,
    NoneRelationFoundError,
    ReferencedLinkNotCachedError,
    TruncatedModelNameCausedCollisionError,
)
from balto.adapters.exceptions.compilation import (
    ApproximateMatchError,
    ColumnTypeMissingError,
    DuplicateMacroInPackageError,
    DuplicateMaterializationNameError,
    MacroNotFoundError,
    MaterializationNotAvailableError,
    MissingConfigError,
    MissingMaterializationError,
    MultipleDatabasesNotAllowedError,
    NullRelationCacheAttemptedError,
    NullRelationDropAttemptedError,
    QuoteConfigTypeError,
    RelationReturnedMultipleResultsError,
    RelationTypeNullError,
    RelationWrongTypeError,
    RenameToNoneAttemptedError,
    SnapshotTargetIncompleteError,
    SnapshotTargetNotSnapshotTableError,
    UnexpectedNonTimestampError,
)
from balto.adapters.exceptions.connection import (
    FailedToConnectError,
    InvalidConnectionError,
)
from balto.adapters.exceptions.database import (
    CrossDbReferenceProhibitedError,
    IndexConfigError,
    IndexConfigNotDictError,
    UnexpectedDbReferenceError,
)
